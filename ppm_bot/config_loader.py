import logging
import os

from yaml import safe_load


logger = logging.getLogger(__name__)


def get_conf_path():
    path = os.path.abspath(__file__)
    split_path = path.split(os.sep)
    while split_path[-1] != "ppm-bot":
        split_path.pop()
    split_path.append("conf")
    return os.sep.join(split_path)


def load_config(*conf_files: str):
    if not conf_files:
        default_file_names = ("config.default.yaml", "config.local.yaml")
        conf_files = (os.path.join(get_conf_path(), file) for file in default_file_names)
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
