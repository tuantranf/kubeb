import os
import shutil
import codecs
import yaml

from dotenv import dotenv_values

from jinja2 import Environment, FileSystemLoader

kubeb_directory = '.kubeb' + os.path.sep
config_file = kubeb_directory + "config.yml"
helm_value_file = kubeb_directory + "helm-values.yml"
install_script_file = kubeb_directory + "install.sh"
uninstall_script_file = kubeb_directory + "uninstall.sh"

docker_file = os.path.join(os.getcwd(), "Dockerfile")
docker_directory = os.path.join(os.getcwd(), "docker")

template_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), './templates/')) + os.path.sep
helm_template_directory = template_directory + "helm"

_marker = object()
_shebang = "#!/usr/bin/env bash"

def config_file_exist():
    return os.path.isfile(config_file)


def docker_file_exist():
    return os.path.isfile(docker_file)


def init_config_dir():
    directory = os.path.join(os.getcwd(), kubeb_directory)
    if not os.path.isdir(directory):
        os.makedirs(directory)


def remove_config_dir():
    directory = os.path.join(os.getcwd(), kubeb_directory)
    if os.path.isdir(directory):
        shutil.rmtree(directory)


def generate_config_file(name, user, template, image, local, env):
    init_config_dir()

    values = dict(
        name=name,
        template=template,
        user=user,
        image=image,
        local=local,
    )

    with open(config_file, "w") as fh:
        fh.write(yaml.dump(values,
                           default_flow_style=False,
                           line_break=os.linesep))

    environments = dict()
    environments[env] = dict(
        name=env
    )

    set_value('environments', environments, config_file)
    set_value('current_environment', env, config_file)

def generate_docker_file(template):
    work_dir = os.getcwd()
    template_dir = template_directory + template

    docker_file_src = os.path.join(template_dir, 'Dockerfile')
    docker_file_dst = os.path.join(work_dir, 'Dockerfile')
    shutil.copy(docker_file_src, docker_file_dst)

    # .dockerignore
    ignore_src = os.path.join(template_dir, '.dockerignore')
    ignore_dst = os.path.join(work_dir, '.dockerignore')
    shutil.copy(ignore_src, ignore_dst)

    # copy docker-data file
    if os.path.isdir(docker_directory):
        shutil.rmtree(docker_directory)
    shutil.copytree(os.path.join(template_dir, 'docker'), docker_directory)


def generate_helm_file(template, image, tag, env):
    template_dir = template_directory + template

    values = dotenv_values(kubeb_directory + ".env." + env)
    print(values)

    values = dict(
        image=image,
        tag=tag,
        env_vars=dict()
    )

    jinja2_env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True)
    content = jinja2_env.get_template('helm-values.yaml').render(values)
    with open(helm_value_file, "w") as fh:
        fh.write(content)


def remove_docker_file():
    if docker_file_exist():
        os.remove(docker_file)

    docker_ignore = os.path.join(os.getcwd(), '.dockerignore')
    os.remove(docker_ignore)

    directory = os.path.join(os.getcwd(), 'docker')
    if os.path.isdir(directory):
        shutil.rmtree(directory)


def clean_up():
    remove_config_dir()
    remove_docker_file()


def generate_script_file(name, template):
    chart_info_file = os.path.join(template_directory + template, "info.yaml")
    chart_name = get_value('chart_name', chart_info_file)
    official = get_value('official', chart_info_file)

    # install script
    with open(install_script_file, "w") as file:
        install_commands = [_shebang]
        if not official:
            repository = get_value('repository', chart_info_file)
            install_commands.append("helm repo add " + repository["name"] + " " + repository["url"])
            install_commands.append("helm repo update")

        install_commands.append("helm upgrade --install --force " + name + " -f " + helm_value_file + " " + chart_name + " --wait")
        file.write("\n".join(install_commands))

    # uninstall script
    with open(uninstall_script_file, "w") as file:
        unintall_commands = [_shebang]
        unintall_commands.append("helm delete --purge " + name)
        file.write("\n".join(unintall_commands))


def set_value(key_name, value, file):
    config = get_yaml_dict(file)
    if not config:
        config = {}

    if type(value) is dict:
        for key in value.keys():
            config.setdefault(key_name, {})[key] = value[key]
    else:
        config[key_name] = value

    with codecs.open(file, 'w', encoding='utf8') as f:
        f.write(yaml.dump(config, default_flow_style=False,
                          line_break=os.linesep))


def get_value(key_name, file, default=_marker):
    value = None
    config = get_yaml_dict(file)
    if config:
        try:
            value = config[key_name]
        except KeyError:
            value = None

    if value is None and default != _marker:
        return default

    return value


def get_yaml_dict(filename):
    try:
        with codecs.open(filename, 'r', encoding='utf8') as f:
            return yaml.load(f)
    except IOError:
        return {}


def generate_environment_file(env, template):
    work_dir = os.getcwd()
    template_dir = template_directory + template

    docker_file_src = os.path.join(template_dir, '.env.sample')
    docker_file_dst = os.path.join(work_dir, '.env.' + env)
    shutil.copy(docker_file_src, docker_file_dst)