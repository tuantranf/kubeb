import os

import subprocess

from . import file_util as file


def build_command(image, tag):
    return "docker build -t " + image + ':' + tag + ' ' + os.getcwd()


def install_command():
    return "bash " + file.install_script_file


def uninstall_command():
    return "bash " + file.uninstall_script_file


def run(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    (output, err) = p.communicate()

    p_status = p.wait()

    return p_status, output, err
