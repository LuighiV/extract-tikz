from pathlib import Path


def load_file(file):
    with open(Path(file), 'r', encoding="utf-8") as f:
        contents = f.read()

    return contents
