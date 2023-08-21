# Python script for extracting tikz figures from document

## Requirements

To compile the extracted files it is required to have and active LaTeX
environment, specifically the script `latexmk` which is used in this program.
It is provided by any distribution, either TeXLive or MikTeX.

Also, for the conversion to images, it is required the `poppler`. If it wasn't
packaged with your OS, please install it. In the case of ArchLinux, it could
be:

```
sudo pacman -S poppler
```

## Installation

To install this package you must build and install following the procedure
suggested for setuptools https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html.

```
pip install --upgrade setuptools
python -m build .
python install .
```

You can also use the scrip from the current source by:
```
pip install -r requirements.txt
```

## How to use

The script could be used installed in your local environment, or directly from the
location of the package source.

If you have installed it, the command name is `extracttikz` and admits the next
options:

```
extracttikz [options] sourcefile.tex
```

**Options:**

* `-h, --help`

  Show this help message and exit

* `-l LOGLEVEL, --log-level=LOGLEVEL`

  Set log level. Available options: critical, error, warning, info, debug

* `-o FOLDER, --output-folder=FOLDER`

  Save to output folder

* `--overwrite`

  Overwrite existing extracted files in directory

* `-B, --build`

  Build extracted tikzpictures

* `-b FOLDER, --build-folder=FOLDER`

  Save compilation result pdf to build folder

* `-E, --export`

  Export built pdfs to images

* `-e FOLDER, --export-folder=FOLDER`

  Save converted image to export folder

* `--only-build`

  Only build files in directory

* `--only-export`

  Only export images from pdf

* `--export-fmt=FORMAT`

  Format for exported images

* `--export-dpi=DPI`

  DPI for exported images


## Cases of use

### General workflow

Normally, we can have a LaTeX project that can have the following structure:
```
- contents/ 
   |- introduction.tex
   |- theory.tex
   |- design.tex
   |- ...
- thesis.tex
```

The main tex file here is `thesis.tex` which includes several `\input` commands
to include the subfiles.

#### Only extract 

Then, the aim is to extract all the tikzpictures environments in individual
files which can compile and export to images.

To perform that we can use the following command:
```
extracttikz thesis.tex
```

We can specify the folder by `--output-folder=<foldername>` otherwise, it will
use `output` relative to the path from which is run the command.

If we run again the command, it will not generate again the files as they
exist in the folder. However, we can force the generation (for example, to
update with latest changes in original document), by adding the option
`--overwrite`:
```
extracttikz --overwrite thesis.tex
```

The resulting files are located under the output folder and will have the
following structure:
```
- output/ 
   |- ch01-002-image_label.tex
   |- ch04-002-image_label.tex
   |- ...
   |- a01-005-image_label.tex
```

Where the file name comes from the chapter number where it is located, the
figure from which it comes from and the label of the figure environment where
the tikzpicture is placed.

> 📝**Note:** the tikzpictures are only exported if they are inside a figure
> environment, otherwise they will be skipped.

#### Extract build and export

If we want to also build and export the tikzpicture into images, we can use the
options `-B` and `-E` to perform such actions:
```
extracttikz -B -E thesis.tex
```
Some important notes to highlight here are:

+ If the options are appended after files were generated, as a second command, it will only
    apply to new extracted files (if doesn't have changes, it will not generate
    anything). To avoid that, you can append the option `--overwrite`.

+ If you only append `-B` it will only build the pdfs, but if you append only
    `-E` it won't do anything as the export stage requires the build first.

+ The directory where the compilation results (pdfs) are placed is the declared by the
    option `--build-folder=folder` otherwise it will take the default `build` relative 
    to the path from which the command is executed.

+ The directory where the exported images are placed is the declared by the
    option `--export-folder=folder` otherwise it will take the default `exported` relative 
    to the path from which the command is executed.

We also have the option to specify the exported format or the DPI for exported
images by the options `--export-fmt` and `--export-dpi`, respectively. For
example:
```
extracttikz --overwrite -B -E --export-dpi=1000 --export-fmt=png thesis.tex
```

### Only build pdfs

Sometimes, we just require building the list of tikzpictures that are extracted
in the output folder. 
```
extracttikz --only-build 
```
> 📝**Note:** This will export **ALL** the tex files in the output folder,
> either the default one or the declared by the option `--output-folder`.

### Only export to images

This can be followed by another option that only export the list of pdf files
that are located in the build folder to images.
```
extracttikz --only-export --export-dpi=1000 --export-fmt=png
```
> 📝**Note:** Equally to the previous option, it will convert **ALL** the pdf
> files located in the build folder, either the default one or the declared by
> the option `--output-build`.

## License

Copyright 2023 Luighi Viton-Zorrilla

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
