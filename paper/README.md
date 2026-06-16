# LaTeX Paper Package

This folder is the Overleaf-ready paper package.

## Main Files

- `main.tex`: paper source.
- `references.bib`: bibliography stub.
- `figures/`: paper figures copied from the canonical analysis package.
- `tables/`: CSV result tables and manifest copied from the canonical analysis package.

## Local Compile

```bash
cd paper_latex
latexmk -pdf -interaction=nonstopmode main.tex
```

The expected output is `main.pdf`.

## Overleaf Workflow

Upload the whole `paper_latex/` folder to Overleaf as a new project. The folder is self-contained and should compile without needing the rest of the repo.

For now, `main.tex` is intentionally one file. Once the paper prose stabilizes, we can split it into sections or swap in a workshop template.

## Source of Truth

The canonical result data still lives in:

```text
artifacts/robomme_cross_session_results
```

This LaTeX folder contains a paper-ready copy of the figures and tables for writing and Overleaf review.
