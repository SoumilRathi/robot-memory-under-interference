# Benchmarking Robot Memory Under Interference

**A cross-session benchmark for memory-augmented VLAs.**

Robots deployed in the real world accumulate histories across many sessions, users, and tasks. A useful memory system should preserve relevant prior experience even when unrelated experience appears between the useful memory and the current task.

This repository packages RoboMME-Interference, a cross-session interference protocol built on RoboMME-style robot memory tasks. We evaluate memory-augmented VLA variants under histories containing a relevant lesson session plus zero or more unrelated distractor sessions.

## TL;DR

- **Protocol:** RoboMME-Interference.
- **Benchmark:** cross-session robot memory under interference.
- **Conditions:** `no-history`, `k0`, `k1`, `k3`, `k7`.
- **Scale:** 9 task families, 9 systems, 18,450 rollouts, 369 / 369 complete result cells.
- **Main result:** perceptual memory variants help strongly when relevant memory is nearby and degrade as distractor sessions increase.
- **Best system in this grid:** FrameSamp-Modul.

## Headline Result

| System | No history | k0 | k1 | k3 | k7 |
| --- | ---: | ---: | ---: | ---: | ---: |
| pi0.5 baseline | 17.3% | - | - | - | - |
| FrameSamp-Modul | 18.2% | 45.3% | 38.4% | 30.0% | 19.3% |
| TokenDrop-Modul | 17.1% | 35.3% | 30.9% | 23.6% | 19.8% |
| FrameSamp-Context | 17.8% | 26.7% | 18.7% | 18.7% | 17.8% |
| FrameSamp-Expert | 17.6% | 27.1% | 20.9% | 19.6% | 19.6% |
| TokenDrop-Context | 13.8% | 22.9% | 19.1% | 15.3% | 13.1% |
| TokenDrop-Expert | 16.9% | 27.3% | 20.2% | 15.6% | 14.0% |
| Recurrent-TTT-Expert | 16.0% | 18.0% | 16.4% | 16.2% | 15.6% |
| Recurrent-TTT-Context | 16.9% | 15.3% | 16.2% | 17.6% | 14.0% |

Full confidence intervals and paired bootstrap comparisons are in [`results/analysis/tables`](results/analysis/tables).

## Repository Structure

```text
.
├── BENCHMARK_PROTOCOL.md
├── RESULTS.md
├── REPRODUCING.md
├── paper/
│   ├── main.tex
│   ├── main.pdf
│   ├── figures/
│   └── tables/
├── results/
│   ├── canonical_rollouts.csv
│   ├── MANIFEST.json
│   ├── coverage.csv
│   └── analysis/
├── scripts/
│   ├── analyze_cross_session_results.py
│   └── create_cross_session_protocol_figure.py
└── website/
    ├── index.html
    ├── styles.css
    └── assets/
```

## Quick Start

Regenerate analysis tables and figures:

```bash
python3 scripts/analyze_cross_session_results.py --results-dir results
```

Compile the paper locally:

```bash
cd paper
latexmk -pdf -interaction=nonstopmode main.tex
```

Open the website locally:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`. The root page redirects to `website/`.

## Relationship to RoboMME

This project builds on the RoboMME-style robot memory evaluation setting. RoboMME-Interference is a complementary protocol, not a new simulator benchmark: it measures how memory systems behave when relevant prior experience is mixed with unrelated prior sessions.

## License

Code, scripts, website source, and benchmark implementation are licensed under Apache-2.0. Result CSVs, generated tables, generated figures, and benchmark result artifacts are licensed under CC BY 4.0. Paper text is excluded from the repository license unless otherwise stated.

## Status

This is a release candidate package. Before wider public launch, finalize:

- paper citations,
- final website copy,
- GitHub Pages deployment,
- optional external feedback from RoboMME authors.
