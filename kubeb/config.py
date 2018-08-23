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
