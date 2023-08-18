from pathlib import Path
import re

from extracttikz.io.load import load_file
from extracttikz.io.path import build_path_if_not_absolute


def build_start_env(name):
    return "\\begin{{{}}}".format(name)


def build_end_env(name):
    return "\\end{{{}}}".format(name)


def build_package_declaration(package):
    return "\\usepackage{{{}}}".format(package)


def build_package_declaration_pattern(package):
    return "\\\\usepackage(\\[.*\\])?\\{{{}\\}}".format(package)


def match_comments(text):
    return re.findall("(?<!\\\\)(\\%.*\\n)", text)


def delete_comments(text):
    return re.sub("(?<!\\\\)(\\%.*\\n)", "", text)


def match_env(name, text):

    pattern = "{}.*?{}".format(re.escape(build_start_env(name)),
                               re.escape(build_end_env(name)))
    # print(pattern)
    return re.findall(pattern, text, re.DOTALL)


def check_package(package, text):

    return re.search(build_package_declaration_pattern(package), text)


def strip_content(text):

    list_document = match_env("document", text)
    if len(list_document) > 0:
        pattern = "{}|{}".format(re.escape(build_start_env("document")),
                                 re.escape(build_end_env("document")))
        return re.sub(pattern, "", list_document[0])

    return text


def delete_standalone(text):

    pattern = "(?>\\\\ifstandalone).*?\\\\fi"
    return re.sub(pattern, "", text, 0, re.DOTALL)


def match_chapters(text):

    pattern = "\\\\chapter(?>\\[(.*?)\\])?\\{(.*?)\\}[ \\s]*(?>\\\\label\\{(.*?)\\})?"
    return re.findall(pattern, text, re.DOTALL)


def get_inputs(text):

    pattern = "\\\\input\\{(.*?)\\}|\\\\include\\{(.*?)\\}"
    return re.findall(pattern, text)


def split_inputs(text):
    pattern = "(\\\\input\\{.*?\\}|\\\\include\\{.*?\\})"
    return re.split(pattern, text)


def split_figure(text):

    pattern = "({}.*?{})".format(re.escape(build_start_env("figure")),
                                 re.escape(build_end_env("figure")))
    return re.split(pattern, text, 0, re.DOTALL)


def clean_document(text):
    return delete_standalone(strip_content(text))


def load_clean_file(file_path, clean, prefix):

    full_path = build_path_if_not_absolute(file_path, prefix)
    contents = load_file(full_path)
    if clean:
        contents = clean_document(contents)

    return contents


def load_input_from_text(text, clean=True, prefix=""):

    list_inputs = get_inputs(text)
    if (len(list_inputs) > 0):
        input_path = list_inputs[0]
        if (input_path[0] is not None):
            file_path = input_path[0]
        elif (input_path[1] is not None):
            file_path = input_path[1]
        else:
            return text

        return load_clean_file(file_path, clean, prefix)

    return text


def expand_inputs(text, prefix):

    no_comments = delete_comments(text)
    n_list = list(map(lambda x: load_input_from_text(
        x, True, prefix), split_inputs(no_comments)))

    return "".join(n_list)


def parse_tikz(text):

    pattern = "{}.*?({}.*?{}).*?\\\\label\\{{(.*?)\\}}.*?{}".format(
        re.escape(build_start_env("figure")),
        re.escape(build_start_env("tikzpicture")),
        re.escape(build_end_env("tikzpicture")),
        re.escape(build_end_env("figure")))
    # print(pattern)
    return re.findall(pattern, text, re.DOTALL)


def has_tikz(text):

    pattern = "{}.*?({}.*?{}).*?\\\\label\\{{(.*?)\\}}.*?{}".format(
        re.escape(build_start_env("figure")),
        re.escape(build_start_env("tikzpicture")),
        re.escape(build_end_env("tikzpicture")),
        re.escape(build_end_env("figure")))
    # print(pattern)
    if re.search(pattern, text, re.DOTALL) is not None:
        return True
    return False


def has_figure(text):

    pattern = "({}.*?{})".format(
        re.escape(build_start_env("figure")),
        re.escape(build_end_env("figure")))
    # print(pattern)
    if re.search(pattern, text, re.DOTALL) is not None:
        return True
    return False


def has_appendix(text):
    pattern = "\\\\appendix"

    if re.search(pattern, text) is not None:
        return True
    return False


def split_appendix(text):

    pattern = "\\\\appendix"

    return re.split(pattern, text)


def extract_tikz(text):

    last_chapter = ()
    list_tikz = []
    count_figure = 0
    count_tikz = 0
    count_chapter = 0
    count_figure_in_chapter = 0
    count_tikz_in_chapter = 0
    is_appendix = False

    for element in split_figure(text):
        if has_figure(element):
            count_figure += 1
            count_figure_in_chapter += 1
            if has_tikz(element):
                count_tikz += 1
                count_tikz_in_chapter += 1
                tikz = parse_tikz(element)
                list_tikz.append({"tikz": tikz,
                                  "chapter": last_chapter,
                                  "counter": {
                                      "chapter": count_chapter,
                                      "figure": count_figure,
                                      "tikz": count_tikz,
                                      "figure_in_chapter": count_figure_in_chapter,
                                      "tikz_in_chapter": count_tikz_in_chapter,
                                  },
                                  "is_appendix": is_appendix})

        else:

            if has_appendix(element):
                is_appendix = True
                count_chapter = 0
                list_appendix = split_appendix(element)
                element = list_appendix[-1]

            list_chapters = match_chapters(element)
            if len(list_chapters) > 0:
                count_chapter += len(list_chapters)
                count_figure_in_chapter = 0
                count_tikz_in_chapter = 0
                last_chapter = list_chapters[-1]

    return list_tikz

# Plan:
# parse document
# split tikz
# non tikz extract sections
# build_tikz_file_name
# create new file and replace tikz by input
