from pathlib import Path

from extracttikz.io.load import load_file
from extracttikz.io.save import save_file
from extracttikz.parser.tex import extract_tikz, clean_document, expand_inputs
from extracttikz.builder.tex import build_tex_file_contents
from extracttikz.builder.name import build_file_name
from extracttikz.compiler.latexmk import LatexMK
from extracttikz.converter.pdftoimage import convert_pdf


def extract_tikz_from_file(filename, expand=True):

    filename = Path(filename)
    contents = load_file(filename)

    if expand:
        contents = expand_inputs(
            clean_document(contents), str(
                filename.parent))

    return extract_tikz(contents)


def refactor_extracted_tikz(parser):

    return {
        # take only the first tikz in figure
        "content": parser["tikz"][0][0],
        # take only the first tikz in figure
        "figure_label": parser["tikz"][0][1],
        "chapter_short": parser["chapter"][0],
        "chapter_long": parser["chapter"][1],
        "chapter_label": parser["chapter"][2],
        "count_chapter": parser["counter"]["chapter"],
        "count_figure": parser["counter"]["figure"],
        "count_tikz": parser["counter"]["tikz"],
        "count_figure_in_chapter": parser["counter"]["figure_in_chapter"],
        "count_tikz_in_chapter": parser["counter"]["tikz_in_chapter"],
        "is_appendix": parser["is_appendix"]
    }


def refactor_list_extracted(list_tikz):

    return map(refactor_extracted_tikz, list_tikz)


def create_tex_filename(structured_tikz):

    return "".join([build_file_name(
        structured_tikz["count_chapter"],
        structured_tikz["is_appendix"],
        structured_tikz["count_figure_in_chapter"],
        structured_tikz["figure_label"]), ".tex"])


def generate_files(l_structured_tikz, folder, overwrite=True):

    folder = Path(folder)
    l_filepaths = []
    for structured_tikz in l_structured_tikz:
        structured_tikz["filename"] = create_tex_filename(structured_tikz)
        content = build_tex_file_contents(**structured_tikz)
        filepath = folder / structured_tikz["filename"]
        if not filepath.exists() or (filepath.exists() and overwrite):
            save_file(filepath, content)
            l_filepaths.append(filepath)

    return l_filepaths


def generate_files_from_tex(filename, expand=True, folder="output",
                            overwrite=True):

    return generate_files(
        refactor_list_extracted(
            extract_tikz_from_file(
                filename,
                expand)),
        folder,
        overwrite)


def compile_file(compiler, filepath):

    return compiler.run(filepath)


def compile_list_files(list_files):

    compiler = LatexMK()
    list_outputs = []
    for file in list_files:
        outputfile = compile_file(compiler, file)
        list_outputs.append(outputfile)

    return list_outputs


def export_pdf(pdfpath, outdir="exported", extension=".jpg"):

    imagepath = Path(outdir) / "".join([Path(pdfpath).stem,
                                       extension])

    convert_pdf(pdfpath, imagepath)

    return imagepath


def export_list_pdf(list_pdfs, outdir="exported", extension=".jpg"):

    list_outputs = []
    for pdffile in list_pdfs:
        outputfile = export_pdf(pdffile, outdir, extension)
        list_outputs.append(outputfile)

    return list_outputs
