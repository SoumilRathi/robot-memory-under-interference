# Analysis Package

Generated tables and figures for the RoboMME-Interference grid, built from [`../canonical_rollouts.csv`](../canonical_rollouts.csv) by [`../../scripts/analyze_cross_session_results.py`](../../scripts/analyze_cross_session_results.py). Coverage: 18,450 / 18,450 rollouts across 9 task families × 9 systems × 5 conditions (`pi05_baseline` is evaluated only under `no-history`).

## Tables

- `tables/main_success_rates.csv` — success rate by system and condition, with Wilson 95% intervals.
- `tables/family_success_rates.csv` — the same, per task family.
- `tables/difficulty_success_rates.csv` — success rate by system and difficulty.
- `tables/effect_sizes.csv` — condition differences (k0/k1/k3/k7 minus no-history, and k0 minus k7).
- `tables/memory_lift_vs_no_history.csv` — each variant's lift over its own no-history rate, with 95% intervals.
- `tables/variant_condition_stats.csv`, `tables/family_variant_condition_stats.csv`, `tables/variant_difficulty_stats.csv` — the underlying success / n counts.

## Figures

- `figures/overall_plain_success_by_condition.png` — headline success curve across all systems.
- `figures/per_family_plain_success_small_multiples.png` — per-family curves.
- `figures/framesamp_modul_family_heatmap.png` — strongest variant, family × condition.
- `figures/difficulty_plain_success.png` — success by difficulty.
- `figures/memory_lift_vs_no_history.png`, `figures/k0_lift_ranking.png` — supporting lift views.

Figures use plain success rates rather than lift: the no-history floor differs by checkpoint and integration mechanism, so plain rates put every system on the same scale.
