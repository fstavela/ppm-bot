from pathlib import Path


def get_data_path():
    path = Path(__file__)
    while path.name != "tests":
        path = path.parent
    path = path.joinpath("data")
    return str(path)
