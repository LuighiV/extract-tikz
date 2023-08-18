from string import Template

from extracttikz.config import tex_template


def build_tex_file_contents(**fields):

    t = Template(tex_template)
    return t.substitute(**fields)
