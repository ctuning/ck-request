# generate bbl in the format understandable by CK
ck replace_string_in_file fgg.misc --file=paper.tex --string=ACM-Reference-Format --replacement=abbrv

pdflatex paper
bibtex paper

ck convert_to_live_ck_report # --output=interactive-ck-article.html

ck replace_string_in_file fgg.misc --file=paper.tex --string=abbrv --replacement=ACM-Reference-Format
