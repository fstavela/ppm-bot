import logging
import os

import pytest

from ppm_bot.config_loader import load_config
from tests.utils import get_data_path


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

valid_config_1_path = os.path.join(get_data_path(), "conf", "valid_config_1.yaml")
valid_config_2_path = os.path.join(get_data_path(), "conf", "valid_config_2.yaml")
empty_config_path = os.path.join(get_data_path(), "conf", "empty_config.yaml")
invalid_config_path = os.path.join(get_data_path(), "conf", "invalid_config.yaml")

valid_config_1 = {
    "test_field1": {
        "nested_field1": "test value",
        "nested_field2": {"double_nested_field": "test value 2"},
    },
    "test_field2": "test value 3",
}
valid_config_2 = {"test_field2": "second value", "test_field3": "third value"}


def test_config_loader_default():
    config = load_config()
    assert config


def test_config_loader_not_found_all():
    assert load_config("testing1.yaml", "testing2.yaml") == {}


def test_config_loader_not_found_partially():
    config = load_config("testing1.yaml", valid_config_1_path, "testing2.yaml")
    assert config == valid_config_1


def test_config_loader_only_one():
    assert load_config(valid_config_1_path) == valid_config_1
    assert load_config(valid_config_2_path) == valid_config_2


def test_config_loader_multiple_files():
    config = load_config(valid_config_1_path, valid_config_2_path)
    assert config == {**valid_config_1, **valid_config_2}

    config = load_config(valid_config_2_path, valid_config_1_path)
    assert config == {**valid_config_2, **valid_config_1}


def test_config_loader_invalid_files():
    with pytest.raises(Exception):
        load_config(invalid_config_path)


def test_config_loader_empty_file():
    assert load_config(empty_config_path) == {}


def test_config_loader_multiple_files_with_empty():
    assert load_config(valid_config_1_path, empty_config_path) == valid_config_1
