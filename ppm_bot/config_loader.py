import logging
from typing import Iterable

from yaml import safe_load


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def load_config(conf_files: Iterable[str] = ("conf/config.default.yaml", "conf/config.local.yaml")):
    config = {}
    for file_name in conf_files:
        try:
            with open(file_name, "r") as file:
                try:
                    config = {**config, **safe_load(file)}
                except Exception as exc:
                    logger.error(f"Error while loading {file_name}")
                    raise exc
        except FileNotFoundError:
            logger.debug(f"{file_name} not found.")
    return config
