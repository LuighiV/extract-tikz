import os

from pdf2image.pdf2image import convert_from_path
from pathlib import Path


def convert_pdf(pdfpath, imagepath=None, extension=".jpg", dpi=200):


    transparent = bool(extension==".png")

    images = convert_from_path(pdfpath, dpi=dpi, use_pdftocairo=True,
                               transparent=transparent)

    # Only export first page
    if imagepath is None:
        imagepath = Path(pdfpath).parent / "".join([Path(pdfpath).stem,
                                                    extension])

    directory = os.path.dirname(imagepath)
    Path(directory).mkdir(parents=True, exist_ok=True)
    images[0].save(imagepath)
