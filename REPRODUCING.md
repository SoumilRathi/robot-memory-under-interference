# Reproducing

## Requirements

For result analysis:

- Python 3.10+
- `pandas`
- `numpy`
- `matplotlib`

For paper compilation:

- LaTeX distribution with `latexmk`.

## Regenerate Analysis

From the repository root:

```bash
python3 scripts/analyze_cross_session_results.py --results-dir results
```

This regenerates:

- `results/analysis/tables/*.csv`
- `results/analysis/figures/*.png`
- `results/analysis/figures/*.pdf`
- `results/analysis/analysis_manifest.json`

## Regenerate Protocol Figure

```bash
python3 scripts/create_cross_session_protocol_figure.py
```

This writes:

- `paper/figures/protocol_diagram.png`
- `paper/figures/protocol_diagram.pdf`

## Compile Paper

```bash
cd paper
latexmk -pdf -interaction=nonstopmode main.tex
```

Output:

- `paper/main.pdf`

## Run Website Locally

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

## Notes

The repository contains the final rollout results and analysis package. It does not contain simulator checkpoints, raw rollout videos, or per-step action traces.
