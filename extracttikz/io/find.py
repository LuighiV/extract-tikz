from pathlib import Path


def find_files(directory, extension):

    return sorted(Path(directory).glob("*{}".format(extension)))
