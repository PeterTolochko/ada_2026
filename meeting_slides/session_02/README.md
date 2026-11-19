# Session 2 slides

Edit `main.tex` in this directory. It is a standalone LaTeX Beamer source with native TikZ diagrams and presenter notes. It follows session 1's style and keeps only pagination in the footer.

The compiled classroom PDF is `../ADA_III_Meeting_02.pdf`.

Compile with the Codex LaTeX editor, or run `latexmk -pdf main.tex` from this directory. To include presenter notes, change `\setbeameroption{hide notes}` to `\setbeameroption{show notes}`.

The timed core is 180 minutes including a 15-minute break and a 25-minute R practical. The final four slides are optional appendix material, outside the timed core. The teaching plan and exercise answers are in `../Session_02_teaching_guide.md` and in the LaTeX notes.

Companion practical: `../../code/SNA_Practical_01_02.Rmd`, with a rendered HTML version alongside it. The combined workbook begins with igraph construction, inspection, graph editing, and plots, then covers both lectures’ measures and interpretation. Advanced calculations are optional.
