import os
import time

import click
# from dotenv import dotenv_values

from kubeb.core import Kubeb, pass_kubeb
from kubeb import file_util, config, command

@click.group()
@click.version_option('0.0.1')
@click.pass_context
def cli(ctx):
    ctx.obj = Kubeb()

@cli.command()
@click.option('--name', '-n',
              default=lambda: os.path.basename(os.getcwd()),
              prompt='Release name',
              help='Release name.')
@click.option('--user', '-n',
              default=lambda: os.environ.get('USER', ''),
              prompt='Maintainer name',
              help='Maintainer name.')
@click.option('--template', '-t',
              default='laravel',
              prompt='Release template',
              help='Release template name.')
@click.option('--image',
              default=lambda: os.environ.get('USER', '') + '/' + os.path.basename(os.getcwd()),
              prompt='Docker image name',
              help='Docker image name.')
@click.option('--env',
              default='local',
              prompt='Environment name',
              help='Environment name.')
@click.option('--local',
              is_flag=True,
              help='Using local docker image.')
@click.option('--force',
              is_flag=True,
              help='Overwrite config file.')
@pass_kubeb
def init(kubeb, name, user, template, local, image, env, force):
    """ Init kubeb configuration
        Generate config, script files
        Generate Docker stuff if use --docker option
    """
    if file_util.config_file_exist() and force is False:
        kubeb.log('Kubeb config found. Please update config file or use --force option')
        return

    file_util.generate_config_file(name, user, template, image, local, env)
    file_util.generate_script_file(name, template)
    file_util.generate_environment_file(env, template)

    if local:
        file_util.generate_docker_file(template)

    kubeb.log('Kubeb config file generated in %s', click.format_filename(file_util.config_file))

@cli.command()
@pass_kubeb
def info(kubeb):
    """ Show current configuration
    """
    if not file_util.config_file_exist():
        kubeb.log('Kubeb config file not found in %s', file_util.kubeb_directory)
        return

    config_data = config.load_config()
    print(config_data)

@cli.command()
@click.option('--message', '-m',
              multiple=True,
              help='Release note')
@pass_kubeb
def build(kubeb, message):
    """ Build current application
        Build Dockerfile image
        Add release note, tag to config file
    """
    if not file_util.config_file_exist():
        kubeb.log('Kubeb config file not found in %s', file_util.kubeb_directory)
        exit(1)

    if not message:
        marker = '# Add release note:'
        hint = ['', '', marker]
        message = click.edit('\n'.join(hint))
        msg = message.split(marker)[0].rstrip()
        if not msg:
            msg = ""
    else:
        msg = '\n'.join(message)

    if config.get_local():
        image = config.get_image()
        tag = 'v' + str(int(round(time.time() * 1000)))

        status, output, err = command.run(command.build_command(image, tag))
        if status != 0:
            kubeb.log('Docker image build failed', err)
            return

        kubeb.log(output)
        kubeb.log('Docker image build succeed.')

        config.add_version(tag, msg)

@cli.command()
@click.option('--version', '-v',
              help='Install version.')
@pass_kubeb
def install(kubeb, version):
    """ Install current application to Kubernetes
        Generate Helm chart value file with docker image version
        If version is not specified, will get the latest version
    """
    if not file_util.config_file_exist():
        kubeb.log('Kubeb config file not found')
        return

    if config.get_local():
        deploy_version = config.get_version(version)
        if not deploy_version:
            kubeb.log('No deployable version found')
            return

        kubeb.log('Deploying version: %s', deploy_version["tag"])
        file_util.generate_helm_file(config.get_template(), config.get_image(), deploy_version["tag"], config.get_current_environment())
    else:
        file_util.generate_helm_file(config.get_template(), config.get_image(), "latest", config.get_current_environment())

    status, output, err = command.run(command.install_command())
    if status != 0:
        kubeb.log('Install application failed', err)
        return

    kubeb.log(output)
    kubeb.log('Install application succeed.')

@cli.command()
@click.confirmation_option()
@pass_kubeb
def uninstall(kubeb):
    """Uninstall current application from Kubernetes
    """
    if not file_util.config_file_exist():
        kubeb.log('Kubeb config file not found')
        return

    status, output, err = command.run(command.uninstall_command())
    if status != 0:
        kubeb.log('Uninstall application failed', err)
        return

    kubeb.log(output)
    kubeb.log('Uninstall application succeed.')


@cli.command()
@pass_kubeb
def version(kubeb):
    """Show current application versions
    """
    if not file_util.config_file_exist():
        kubeb.log('Kubeb config file not found in %s', file_util.kubeb_directory)
        return

    versions = config.get_versions()
    if not versions or len(versions) == 0:
        kubeb.log('No version found in %s', file_util.kubeb_directory)
        return

    for version in versions:
        kubeb.log('- %s: %s', version['tag'], version['message'])

@cli.command()
@click.argument('env',
            default='local',
            help='Environment',
            type=str)
@pass_kubeb
def env(kubeb, env):
    """Use environment
    """
    if not file_util.config_file_exist():
        kubeb.log('Kubeb config file not found in %s', file_util.kubeb_directory)
        return

    environment = config.get_env(env)
    if not environment:
        kubeb.log('Environment not found')
        kubeb.log('Initiate environment %s in %s', env, file_util.kubeb_directory)
        file_util.generate_environment_file(env)

    config.set_current_environement(env)
    kubeb.log('Now use %', env)

@cli.command()
@click.confirmation_option()
@pass_kubeb
def destroy(kubeb):
    """Remove all kubeb configuration
    """
    file_util.clean_up()

    kubeb.log('Destroyed config directory %s' % file_util.kubeb_directory)


