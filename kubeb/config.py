from . import file_util


def load_config():
    return file_util.get_yaml_dict(file_util.config_file)


def get_image():
    return file_util.get_value("image", file_util.config_file)


def add_version(tag, message=""):
    version = file_util.get_value('version', file_util.config_file)
    if not version:
        version = []

    version.append(dict(
        tag=tag,
        message=message
    ))

    file_util.set_value("version", version, file_util.config_file)


def get_versions():
    return file_util.get_value('version', file_util.config_file)


def get_version(version=None):
    versions = get_versions()
    if not versions or len(versions) == 0:
        return None

    found_version = None
    if not version:
        found_version = versions[-1]
    else:
        try:
            found_version = next((ver for ver in versions if ver["tag"] == version))
        except StopIteration:
            pass
    return found_version


def get_template():
    return file_util.get_value('template', file_util.config_file)


def get_local():
    return file_util.get_value('local', file_util.config_file)


def get_env(name):
    environments = file_util.get_value('env', file_util.config_file)
    if not environments:
        return None

    environment = None
    try:
        environment = environments.name
    except KeyError:
        pass

    return environment

def add_environement(env):
    environments = file_util.get_value('environments', file_util.config_file)
    if not environments:
        environments = dict()

    environments[env] = dict(
        name=env
    )

    file_util.set_value("environments", env, file_util.config_file)

def set_current_environement(env):
    file_util.set_value("current_environment", env, file_util.config_file)


def get_current_environment():
    return file_util.get_value('current_environment', file_util.config_file)


def get_ext_template():
    return file_util.get_value('ext_template', file_util.config_file)
