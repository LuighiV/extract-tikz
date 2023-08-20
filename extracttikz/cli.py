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

parser.add_option("--overwrite", action="store_true", dest="overwrite",
                  default=False,
                  help="overwrite existing extracted files in directory")

parser.add_option("-B", "--build", action="store_true", dest="build_pdf",
                  default=False, help="build extracted tikzpictures")

parser.add_option("-b",
                  "--build-folder",
                  dest="build_folder",
                  help="save compilation result pdf to build folder",
                  metavar="FOLDER")

parser.add_option("-E", "--export", action="store_true", dest="export_images",
                  default=False, help="export built pdfs to images")

parser.add_option("-e",
                  "--export-folder",
                  dest="export_folder",
                  help="save converted image to export folder",
                  metavar="FOLDER")


def check_folder_option(variable, default_value, option_string):

    if (variable is not None):
        foldername = variable
    else:
        foldername = default_value
        logger.warning(
            "Not folder name provided via {}. Usign default: {}".format(
                option_string, foldername))

    return foldername


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

    DEFAULT_OUTPUT_FOLDER_NAME = "output"
    DEFAULT_BUILD_FOLDER_NAME = "build"
    DEFAULT_EXPORT_FOLDER_NAME = "exported"

    output_folder = check_folder_option(options.output_folder,
                                        DEFAULT_OUTPUT_FOLDER_NAME,
                                        option_string="--output-folder")

    list_files = generate_files_from_tex(filename,
                                         expand=True,
                                         folder=output_folder,
                                         overwrite=options.overwrite)
    logger.debug(list_files)
    logger.info(
        "Extracted {} {}tikzpictures".format(
            len(list_files),
            "" if options.overwrite else "new "))

    if options.build_pdf:

        build_folder = check_folder_option(options.build_folder,
                                           DEFAULT_BUILD_FOLDER_NAME,
                                           option_string="--build-folder")
        pdf_files = compile_list_files(list_files, outdir=build_folder)
        logger.debug(pdf_files)

        if options.export_images:

            export_folder = check_folder_option(
                options.export_folder,
                DEFAULT_EXPORT_FOLDER_NAME,
                option_string="--export-folder")
            image_files = export_list_pdf(pdf_files, outdir=export_folder)
            logger.debug(image_files)

    logger.info("Task finished")
    sys.exit(0)
