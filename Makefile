ueberblick.pdf: ueberblick.tex
	latexmk -pdf $<

ueberblick.pdf-live: ueberblick.tex
	latexmk -pdf -pvc $<

beispiele.pdf: beispiele.tex
	latexmk -pdf $<

beispiele.pdf-live: beispiele.tex
	latexmk -pdf -pvc $<

slides.pdf: slides.tex
	latexmk -pdf $<

slides.pdf-live: slides.tex
	latexmk -pdf -pvc $<

ausarbeitung.pdf: ausarbeitung.tex
	latexmk -pdf $<

ausarbeitung.pdf-live: ausarbeitung.tex
	latexmk -pdf -pvc $<

clean:
	rm -f *.aux *.log *.fls *.out *.fdb_latexmk *.toc
