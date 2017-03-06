

main.pdf: *.tex *.bib
	latexmk -pdf main.tex

clean:
	rm -rf *.aux *.bbl *.blg *.fdb_latexmk main.pdf *.toc