# Reproducing

## Requirements

Python 3.10+ with `pandas`, `numpy`, and `matplotlib`.

## Rebuild the analysis package

From the repository root:

```bash
python3 scripts/analyze_cross_session_results.py --results-dir results
```

This reads [`results/canonical_rollouts.csv`](results/canonical_rollouts.csv) and regenerates:

- `results/analysis/tables/*.csv` — success-rate and effect-size tables with Wilson 95% intervals.
- `results/analysis/figures/*.{png,pdf}` — the analysis figures.
- `results/analysis/analysis_manifest.json`.

## Regenerate the protocol diagram

```bash
python3 scripts/create_cross_session_protocol_figure.py
```

Writes `assets/protocol_diagram.png`, used by the website.

## Run the website locally

```bash
python3 -m http.server 8000      # then open http://localhost:8000
```

## Scope

This repository holds the final rollout results and the analysis package. Simulator checkpoints, raw rollout videos, and per-step action traces are not redistributed here — they come from [RoboMME](https://robomme.github.io/).
