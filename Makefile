ueberblick.pdf: ueberblick.tex
	latexmk -pdf $<

ueberblick.pdf-live: ueberblick.tex
	latexmk -pdf -pvc $<

clean:
	rm -f *.aux *.log *.fls *.out *.fdb_latexmk *.toc
