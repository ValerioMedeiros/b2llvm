
FILES = $(filter-out codeFormat.tex, $(wildcard *.tex))

DEP:=$(FILES:%.tex=%.pdf)

all: $(DEP) clean



%.pdf : %.tex
	pdflatex -shell-escape $<


clean:
	-rm -f *.swp *~ *.out *.aux *.dvi *.ps *.toc *.lof *.log *.lot *.flg *.bbl *.blg *.idx *.ind *.ilg *.snm *.nav *.fig.bak
