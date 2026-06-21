# Results

Success rate (%) by history condition; π₀.₅ is the no-memory floor. Per-cell Wilson 95% intervals are in [`results/analysis/tables/main_success_rates.csv`](results/analysis/tables/main_success_rates.csv).

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

## What the numbers show

- **Adaptive modulation carries the effect.** FrameSamp-Modul and TokenDrop-Modul are the only systems with a large near-session gain: +27.1 and +18.2 percentage points at `k0` over their own no-history rate.
- **That gain is recency, not recall.** As distractor sessions push the lesson back, both decay to the baseline. FrameSamp-Modul falls from 45.3% at `k0` to 19.3% at `k7` — a +1.1 pp residual over no-history. TokenDrop-Modul falls from 35.3% to 19.8% (+2.7 pp).
- **Other integration mechanisms barely move.** Context (concatenation) and Expert (block-wise attention) variants gain little even at `k0` and reach `k7` indistinguishable from the floor.
- **Recurrent memory is flat.** The TTT variants track π₀.₅ across every condition.

## By task difficulty

The memory benefit concentrates on easier tasks. Pooled across conditions, FrameSamp-Modul reaches 38.0% on easy and 28.5% on medium tasks (π₀.₅: 20.9% and 13.9%), but only 15.2% on hard tasks against a 13.0% floor. Full breakdown in [`difficulty_success_rates.csv`](results/analysis/tables/difficulty_success_rates.csv).

## Figures

- [`overall_plain_success_by_condition.png`](results/analysis/figures/overall_plain_success_by_condition.png) — success vs. session distance, all systems.
- [`per_family_plain_success_small_multiples.png`](results/analysis/figures/per_family_plain_success_small_multiples.png) — per-family curves.
- [`framesamp_modul_family_heatmap.png`](results/analysis/figures/framesamp_modul_family_heatmap.png) — strongest variant, family × condition.
- [`difficulty_plain_success.png`](results/analysis/figures/difficulty_plain_success.png) — success by difficulty.

## Data

- [`canonical_rollouts.csv`](results/canonical_rollouts.csv) — every rollout, the source of truth.
- [`coverage.csv`](results/coverage.csv) — cell-level coverage (369 / 369 complete).
- [`analysis/tables/`](results/analysis/tables) — success-rate and effect-size tables with Wilson intervals.
