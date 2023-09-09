from optparse import OptionParser
import sys
from pathlib import Path

from extracttikz.logger import logger, levels, setLoggerLevel
from extracttikz.process import export_list_pdf, generate_files_from_tex, compile_list_files
from extracttikz.io.find import find_files


usage = "usage: %prog [options] inputfile"
parser = OptionParser(usage=usage, prog="extracttikz")
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

parser.add_option("--only-build", action="store_true", dest="only_build",
                  default=False,
                  help="only build files in directory")

parser.add_option("--only-export", action="store_true", dest="only_export",
                  default=False,
                  help="only export images from pdf")

parser.add_option("--export-fmt",
                  dest="export_format",
                  help="format for exported images",
                  metavar="FORMAT")

parser.add_option("--export-dpi",
                  dest="export_dpi",
                  help="DPI for exported images",
                  metavar="DPI")


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

    full_process = options.only_build is False and options.only_export is False

    if len(args) != 1 and full_process:
        parser.error(
            "Incorrect number of arguments. Must provide the input file.")


    if options.loglevel is not None:
        loglevel = options.loglevel
    else:
        loglevel = "info"

    setLoggerLevel(loglevel)

    logger.debug(options)

    DEFAULT_OUTPUT_FOLDER_NAME = "output"
    DEFAULT_BUILD_FOLDER_NAME = "build"
    DEFAULT_EXPORT_FOLDER_NAME = "exported"

    VALID_FORMAT_OPTIONS=["png","jpg","tiff"]
    DEFAULT_EXPORT_IMAGE_FMT="jpg"
    DEFAULT_EXPORT_IMAGE_DPI=200


    list_files=[]
    pdf_files=[]

    if full_process:

        output_folder = check_folder_option(options.output_folder,
                                        DEFAULT_OUTPUT_FOLDER_NAME,
                                        option_string="--output-folder")

        if Path(args[0]).exists():
            filename = args[0]
        else:
            logger.error(
                f"File {args[0]} doesn't exist. Please, provide a valid path ")
            sys.exit(-1)

        list_files = generate_files_from_tex(filename,
                                             expand=True,
                                             folder=output_folder,
                                             overwrite=options.overwrite)
        logger.debug(list_files)
        logger.info(
            "Extracted {} {}tikzpictures".format(
                len(list_files),
                "" if options.overwrite else "new "))

    elif options.only_build:

        output_folder = check_folder_option(options.output_folder,
                                        DEFAULT_OUTPUT_FOLDER_NAME,
                                        option_string="--output-folder")
        list_files = find_files(output_folder, ".tex")
        logger.info("Located {} tikzpictures in folder {}".format( len(list_files), output_folder))



    if (full_process and options.build_pdf) or options.only_build:

        build_folder=check_folder_option(options.build_folder,
                                           DEFAULT_BUILD_FOLDER_NAME,
                                           option_string="--build-folder")
        pdf_files=compile_list_files(list_files, outdir=build_folder)
        logger.debug(pdf_files)

    elif options.only_export:

        build_folder=check_folder_option(options.build_folder,
                                           DEFAULT_BUILD_FOLDER_NAME,
                                           option_string="--build-folder")
        pdf_files = find_files(build_folder, ".pdf")
        logger.info("Located {} pdf in folder {}".format( len(pdf_files),
                                                         build_folder))

    if (full_process and options.export_images and options.build_pdf) or options.only_export:

        export_folder=check_folder_option(
            options.export_folder,
            DEFAULT_EXPORT_FOLDER_NAME,
            option_string="--export-folder")

        if options.export_format:
            if options.export_format in VALID_FORMAT_OPTIONS:
                fmt=options.export_format
            else:
                fmt=DEFAULT_EXPORT_IMAGE_FMT
                logger.warning("Not valid entered format: {}. Default to {}".format(options.export_format,fmt))

        else:
            fmt=DEFAULT_EXPORT_IMAGE_FMT

        extension=".{}".format(fmt)

        if options.export_dpi:
            if options.export_dpi.isdigit():
                dpi=int(options.export_dpi)

            else:
                dpi=DEFAULT_EXPORT_IMAGE_DPI
                logger.warning("Not valid entered DPI: {}. Default to {}".format(options.export_dpi,dpi))

        else:
            dpi=DEFAULT_EXPORT_IMAGE_DPI


        image_files=export_list_pdf(pdf_files,
                                    outdir=export_folder,
                                    extension=extension,dpi=dpi)
        logger.debug(image_files)

    logger.info("Task finished")
    sys.exit(0)
