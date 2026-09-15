# XeLaTeX + BibTeX; no shell escape and no system-specific font paths.
$pdf_mode = 5;
$xelatex = 'xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error %O %S';
$bibtex_use = 2;
$max_repeat = 6;
@default_files = ('main.tex');
