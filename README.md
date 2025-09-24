# IM1202-project

This repository contains a LaTeX document with bibliography that is automatically compiled to PDF using GitHub Actions.

## Files

- `document.tex` - Main LaTeX document
- `references.bib` - Bibliography database
- `.github/workflows/compile-latex.yml` - GitHub Actions workflow for PDF compilation

## Usage

The LaTeX document is automatically compiled to PDF whenever changes are pushed to the main branch. The compiled PDF is available as a workflow artifact.

To compile locally (requires LaTeX installation):
```bash
pdflatex document.tex
bibtex document
pdflatex document.tex
pdflatex document.tex
```

## Workflow

The GitHub Actions workflow:
1. Checks out the repository
2. Compiles the LaTeX document using `xu-cheng/latex-action`
3. Uploads the resulting PDF as an artifact
4. Uploads build logs if compilation fails