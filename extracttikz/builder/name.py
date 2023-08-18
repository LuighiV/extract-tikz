import re


def build_file_name(count_chapter, is_appendix, count_figure_in_chapter,
                    figure_label):
    return "{}{}-{}-{}".format("a" if is_appendix else "ch",
                               repr(count_chapter).zfill(2),
                               repr(count_figure_in_chapter).zfill(3),
                               process_label(figure_label))


def process_label(label):

    nlabel = re.sub(".*?\\:", "", label.lower())

    return re.sub(r'[^a-z0-9_]+', "_", nlabel)
