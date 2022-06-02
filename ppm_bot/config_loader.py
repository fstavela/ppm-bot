import logging
import os
from pathlib import Path

from yaml import safe_load


logger = logging.getLogger(__name__)


def get_conf_path():
    path = Path(__file__)
    while path.name != "ppm-bot":
        path = path.parent
    path = str(path.joinpath("conf"))

    if os.path.isdir(path):
        logger.debug(f"Found conf directory: {path}")
        return path
    raise NotADirectoryError(f"{path} directory not found")


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
