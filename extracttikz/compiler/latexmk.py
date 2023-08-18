from string import Template
from pathlib import Path
from subprocess import PIPE, Popen

import os

from extracttikz.config import wrapper_template
from extracttikz.io.save import save_file


class LatexMK (object):

    def __init__(self, command="latexmk", compiler="pdflatex", outdir="build"):
        self.command = command
        self.compiler = compiler
        self.outdir = outdir
        self.template = wrapper_template
        self.wrapper_contents = ""
        self.wrapper_file = None
        self.filepath = None
        self.full_command = []

    def build_run_command(self, filepath):
        return [
            self.command,
            '-pdf',
            # TODO: investigate error for custome compiler (doesn't compile)
            # '-{compiler}="{compiler} --shell-scape %O %S"'.format(compiler=self.compiler),
            '-interaction="nonstopmode"',
            '-outdir={}'.format(self.outdir),
            str(Path(filepath).absolute())
        ]

    def build_wrapper_filename(self, filepath):
        return "wrapper_{}".format(str(Path(filepath).name))

    def build_output_filename(self, filepath):
        return ".".join([Path(filepath).stem, "pdf"])

    def build_wrapper_file(self, filepath):

        self.wrapper_contents = Template(
            self.template).substitute(
            filename=str(filepath))

        self.wrapper_file = Path(self.outdir) / \
            self.build_wrapper_filename(filepath)

        save_file(self.wrapper_file, self.wrapper_contents)

    def run(self, filepath: str):

        self.filepath = Path(filepath).absolute()
        self.build_wrapper_file(self.filepath)
        self.full_command = self.build_run_command(self.wrapper_file)
        # print(self.full_command)

        try:
            Popen(self.full_command, stdout=PIPE).wait()
        except OSError as e:
            raise e

        self.outputfile = Path(self.outdir) / \
            self.build_output_filename(self.wrapper_file)

        return self.outputfile
