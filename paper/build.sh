#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "=== Compiling LaTeX ==="
mkdir -p build

export TEXINPUTS=".:./sections/:./figures/:"
export BIBINPUTS=".:"
export BSTINPUTS=".:"

pdflatex -output-directory=build main.tex

cp references.bib build/
cd build
bibtex main
cd ..

pdflatex -output-directory=build main.tex
pdflatex -output-directory=build main.tex

echo "=== Done: build/main.pdf ==="
cp build/main.pdf .
echo "Output: main.pdf"
