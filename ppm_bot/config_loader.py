import logging
import os

from yaml import safe_load


logger = logging.getLogger(__name__)


def get_conf_path():
    file_path = os.path.abspath(__file__)
    split_path = file_path.split(os.sep)
    while split_path[-1] != "ppm-bot":
        split_path.pop()
    split_path.append("conf")
    conf_path = os.sep.join(split_path)
    if os.path.isdir(conf_path):
        logger.debug(f"Found conf directory: {conf_path}")
        return conf_path
    raise NotADirectoryError(f"{conf_path} directory not found")


def load_config(*conf_files: str):
    if not conf_files:
        default_file_names = ("config.default.yaml", "config.local.yaml")
        conf_dir = get_conf_path()
        conf_files = (os.path.join(conf_dir, file) for file in default_file_names)
    config = {}
    for file_name in conf_files:
        try:
            with open(file_name, "r") as file:
                try:
                    loaded_conf = safe_load(file)
                    if loaded_conf is None:
                        loaded_conf = {}
                    config = {**config, **loaded_conf}
                except Exception as exc:
                    logger.error(f"Error while loading {file_name}")
                    raise exc
        except FileNotFoundError:
            logger.debug(f"{file_name} not found.")
    return config
