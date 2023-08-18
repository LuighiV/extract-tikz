from dotenv import load_dotenv

load_dotenv()

tex_template = """% $filename
% figure_label: $figure_label
% chapter_label: $chapter_label
% count_chapter: $count_chapter
% count_figure: $count_figure
% count_figure_in_chapter: $count_figure_in_chapter
% count_tikz: $count_tikz
% count_tikz_in_chapter: $count_tikz_in_chapter

$content
"""

wrapper_template = r"""% wrapper_template.tex
\documentclass[class=article]{standalone}
\usepackage[utf8]{inputenc}
\if@spanish
   \usepackage[spanish,es-noshorthands,es-nosectiondot]{babel}
\else
   \usepackage[english]{babel}
\fi
\usepackage[T1]{fontenc}
\usepackage{amsmath, amssymb}
\usepackage{ifxetex}
\ifxetex
   \usepackage{fontspec}
   %\setmainfont{Arial}
\else
\usepackage{newtxtext,newtxmath}
%\usepackage{uarial}
\fi
\ifxetex
   %
\else
\pdfminorversion=7
\pdfsuppresswarningpagegroup=1
\fi
\usepackage[all]{nowidow}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{xcolor}
\usepackage{array}
\usetikzlibrary{arrows.meta}
\usetikzlibrary{decorations}
\usetikzlibrary{decorations.pathreplacing}
\usetikzlibrary{fit}
\usetikzlibrary{graphs}
\usetikzlibrary{intersections}
\usetikzlibrary{matrix}
\usetikzlibrary{patterns}
\usetikzlibrary{positioning}
\usetikzlibrary{shadows}
\usetikzlibrary{shapes.arrows}
\usetikzlibrary{shapes.symbols}
\usetikzlibrary{shapes.geometric}
\usetikzlibrary{shapes.multipart}
\usetikzlibrary{shapes.misc}
\usetikzlibrary{circuits.logic}
\usetikzlibrary{circuits.logic.US}
\usepackage[nooldvoltagedirection]{circuitikz}
\ctikzset{tripoles/mos style/arrows}
\tikzset{>=Stealth}
\usepackage{pgfplots}
\pgfplotsset{compat=1.13} %Setting appropriate configuration
\usetikzlibrary{pgfplots.dateplot}
\usepackage{csquotes}
\usepackage{transparent}

% Required to output only tikzpicture/pgfpicture environments
\usepackage[active,pdftex,tightpage]{preview}
\PreviewEnvironment[]{tikzpicture}
\PreviewEnvironment[]{pgfpicture}

\begin{document}
\input{$filename}
\end{document}
"""
