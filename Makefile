ueberblick.pdf: ueberblick.tex
	latexmk -pdf $<

ueberblick.pdf-live: ueberblick.tex
	latexmk -pdf -pvc $<

slides.pdf: slides.tex
	latexmk -pdf $<

slides.pdf-live: slides.tex
	latexmk -pdf -pvc $<

clean:
	rm -f *.aux *.log *.fls *.out *.fdb_latexmk *.toc
