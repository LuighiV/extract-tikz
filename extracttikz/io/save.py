import os
from pathlib import Path


def save_file(filepath, content):

    directory = os.path.dirname(filepath)
    Path(directory).mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", encoding='utf8') as f:
        f.write(content)

    return
