# This is just a quick hack to test locally
# .............................................................................

all:
	pandoc -f markdown -t latex --pdf-engine=xelatex  --biblatex --bibliography paper.bib paper.md -o paper.tex --template latex.template 
	pdflatex paper.tex
	biber paper
	pdflatex paper.tex

