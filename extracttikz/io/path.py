
from pathlib import Path


def build_path_if_not_absolute(path, prefix):

    new_path = Path(path)
    if (new_path.is_absolute()):
        return new_path

    return Path(prefix) / new_path
