# Benchmarking Robot Memory Under Interference

A cross-session benchmark for memory-augmented vision-language-action policies.

Robots that run for days accumulate experience across many sessions, users, and tasks. A useful memory system has to hold onto a relevant past session even when unrelated sessions pile up in between. This benchmark measures that directly: it places a relevant *lesson* session in the policy's history, inserts *k* unrelated distractor sessions after it, and tests whether the policy can still use the lesson to solve the current task.

It is built directly on **[RoboMME](https://robomme.github.io/)** (Dai et al., ICML 2026). We use RoboMME's tasks, π₀.₅ checkpoints, and released memory-augmented variants; we add the cross-session interference protocol, the evaluation grid, and the analysis.

## At a glance

- **Conditions:** `no-history`, `k0`, `k1`, `k3`, `k7` — the number of unrelated sessions sitting between the lesson and the query.
- **Grid:** 9 task families × 9 systems × 5 conditions × 50 episodes = **18,450 rollouts** (369 / 369 cells complete).
- **Finding:** memory helps sharply when the lesson is recent and decays back to the no-memory baseline as distractors accumulate. The gain belongs almost entirely to adaptive-modulation integration; recurrent variants stay flat.

## Headline result

Success rate (%) by history condition. π₀.₅ is the no-memory floor.

| System | No history | k0 | k1 | k3 | k7 |
| --- | ---: | ---: | ---: | ---: | ---: |
| π₀.₅ (baseline) | 17.3 | – | – | – | – |
| FrameSamp-Modul | 18.2 | **45.3** | 38.4 | 30.0 | 19.3 |
| TokenDrop-Modul | 17.1 | 35.3 | 30.9 | 23.6 | 19.8 |
| FrameSamp-Context | 17.8 | 26.7 | 18.7 | 18.7 | 17.8 |
| FrameSamp-Expert | 17.6 | 27.1 | 20.9 | 19.6 | 19.6 |
| TokenDrop-Context | 13.8 | 22.9 | 19.1 | 15.3 | 13.1 |
| TokenDrop-Expert | 16.9 | 27.3 | 20.2 | 15.6 | 14.0 |
| Recurrent-TTT-Expert | 16.0 | 18.0 | 16.4 | 16.2 | 15.6 |
| Recurrent-TTT-Context | 16.9 | 15.3 | 16.2 | 17.6 | 14.0 |

Per-cell Wilson 95% intervals are in [`results/analysis/tables/main_success_rates.csv`](results/analysis/tables/main_success_rates.csv). More in [RESULTS.md](RESULTS.md).

## Links

- **Website:** https://robotmemorybench.com
- **Paper:** arXiv (forthcoming)
- **Data:** [`results/canonical_rollouts.csv`](results/canonical_rollouts.csv) — every rollout, the source of truth
- **Protocol:** [BENCHMARK_PROTOCOL.md](BENCHMARK_PROTOCOL.md)

## Repository layout

```text
.
├── index.html, research.css, showcase.js   # project website (served via GitHub Pages)
├── BENCHMARK_PROTOCOL.md                    # protocol specification
├── RESULTS.md                               # headline numbers and effects
├── REPRODUCING.md                           # how to regenerate the analysis
├── results/
│   ├── canonical_rollouts.csv               # 18,450 rollouts — source of truth
│   ├── coverage.csv, grid_summary.csv, by_family_condition.csv, by_difficulty.csv
│   ├── MANIFEST.json, SHA256SUMS, README.md
│   └── analysis/                            # generated tables and figures
├── scripts/
│   ├── analyze_cross_session_results.py     # rebuild the analysis package
│   └── create_cross_session_protocol_figure.py
└── assets/                                  # figures and showcase videos
```

## Quick start

```bash
# Rebuild the analysis tables and figures from the canonical rollouts
python3 scripts/analyze_cross_session_results.py --results-dir results

# Serve the website locally
python3 -m http.server 8000      # then open http://localhost:8000
```

## License

Code, scripts, and website source are released under Apache-2.0 ([`LICENSE`](LICENSE)). Result CSVs, tables, and figures are released under CC BY 4.0 ([`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt)). Details in [`LICENSE.md`](LICENSE.md).

## Citation

If you use this benchmark, please cite it ([`CITATION.cff`](CITATION.cff)) and cite RoboMME, which it builds on.
