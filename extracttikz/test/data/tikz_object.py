tikz_appendix = {
    'tikz': [(
        r'\\begin{tikzpicture}\n   \\path[draw, <->, name path=xaxis] (-2,0) coordinate (left) -- (7,0) node[anchor=north] (t) {$t$};\n ;  \\end{tikzpicture}',
        'fig:approximation')],
    'chapter': ('Parameters of performance',
                "Fundamentals on paremeters of performance",
                'ap:fundamentals'),
    'counter': {'chapter': 1, 'figure': 87, 'tikz': 31, 'figure_in_chapter': 4,
                'tikz_in_chapter': 4}, 'is_appendix': True
}

tikz_appendix_refactored = {
    "content": r'\\begin{tikzpicture}\n   \\path[draw, <->, name path=xaxis] (-2,0) coordinate (left) -- (7,0) node[anchor=north] (t) {$t$};\n ;  \\end{tikzpicture}',
    "figure_label": 'fig:approximation',
    "chapter_short": 'Parameters of performance',
    "chapter_long": "Fundamentals on paremeters of performance",
    "chapter_label": 'ap:fundamentals',
    "count_chapter": 1,
    "count_figure": 87,
    "count_tikz": 31,
    "count_figure_in_chapter": 4,
    "count_tikz_in_chapter": 4,
    "is_appendix": True}


tikz_appendix_contents = r"""
% a01-004-approximation.tex
% figure_label: fig:approximation
% chapter_label: ap:fundamentals
% count_chapter: 1
% count_figure: 87
% count_figure_in_chapter: 4
% count_tikz: 31
% count_tikz_in_chapter: 4

\\begin{tikzpicture}\n   \\path[draw, <->, name path=xaxis] (-2,0) coordinate (left) -- (7,0) node[anchor=north] (t) {$t$};\n ;  \\end{tikzpicture}
"""
