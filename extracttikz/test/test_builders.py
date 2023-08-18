
from extracttikz.builder.name import build_file_name, process_label
from extracttikz.builder.tex import build_tex_file_contents
from extracttikz.process import create_tex_filename, refactor_extracted_tikz

from extracttikz.test.data.tikz_object import tikz_appendix_contents, tikz_appendix_refactored, tikz_appendix


def test_process_label():

    assert process_label("fig:figure-test") == "figure_test"
    assert process_label("sec:Section 1") == "section_1"


def test_build_file_name():

    assert build_file_name(
        1, False, 12, "fig:test_figure") == "ch01-012-test_figure"

    assert build_file_name(
        2, True, 14, "fig:test_figure") == "a02-014-test_figure"


def test_build_tex_file_contents():

    refactored = tikz_appendix_refactored.copy()
    refactored["filename"] = create_tex_filename(
        tikz_appendix_refactored)
    assert refactored["filename"] == "a01-004-approximation.tex"
    assert build_tex_file_contents(
        **refactored) == tikz_appendix_contents


def test_refactor():

    assert refactor_extracted_tikz(tikz_appendix) == tikz_appendix_refactored
