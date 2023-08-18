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

* `-o FILE, --output-file=FILE`

  Save to output file

* `-C, --compile`

  Compile files


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
