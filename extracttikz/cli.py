from optparse import OptionParser
import sys
from pathlib import Path

from extracttikz import config
from extracttikz.logger import logger, levels, setLoggerLevel
from extracttikz.process import export_list_pdf, generate_files_from_tex, compile_list_files


usage = "usage: %prog [options] inputfile"
parser = OptionParser(usage=usage, prog="dlgsheet")
parser.add_option("-l", "--log-level", dest="loglevel",
                  help="set log level. Available options: " + ",".join(levels))
parser.add_option("-o", "--output-folder", dest="output_folder",
                  help="save to output folder", metavar="FOLDER")

parser.add_option("-C", "--compile", action="store_true",
                  dest="build_pictures",
                  default=False, help="build extracted pictures")


def main():

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error(
            "Incorrect number of arguments. Must provide the input file.")

    if Path(args[0]).exists():
        filename = args[0]
    else:
        logger.error(
            f"File {args[0]} doesn't exist. Please, provide a valid path ")
        sys.exit(-1)

    if options.loglevel is not None:
        loglevel = options.loglevel
    else:
        loglevel = "info"

    setLoggerLevel(loglevel)

    logger.debug(options)

    DEFAULT_FOLDER_NAME = "output"

    if (options.output_folder is not None):
        foldername = options.output_folder
    else:
        foldername = DEFAULT_FOLDER_NAME
        logger.warning(
            "Not folder name provided via --output-folder. Usign default: " +
            foldername)

    list_files = generate_files_from_tex(filename)
    logger.debug(list_files)
    pdf_files = compile_list_files(list_files)
    logger.debug(pdf_files)

    image_files = export_list_pdf(pdf_files)
    logger.debug(image_files)

    logger.info("Task finished")
