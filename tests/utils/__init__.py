import os


def get_data_path():
    path = os.path.abspath(__file__)
    split_path = path.split(os.sep)
    while split_path[-1] != "tests":
        split_path.pop()
    split_path.append("data")
    return os.sep.join(split_path)
