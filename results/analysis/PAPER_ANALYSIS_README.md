# RoboMME-Interference Analysis Package

This folder contains the first paper-facing analysis pass for the locked cross-session RoboMME result grid.

## Source

- Canonical rollout file: `../canonical_rollouts.csv`
- Coverage: 18,450 / 18,450 expected rollouts
- Grid: 9 task families x 9 memory systems x 5 history conditions, with `pi05_baseline` evaluated once as the no-memory floor

## Primary Tables

- `tables/main_success_rates.csv`: overall success rate by memory system and history condition, with Wilson 95% confidence intervals.
- `tables/family_success_rates.csv`: per-family success rate by memory system and history condition, with Wilson 95% confidence intervals.
- `tables/difficulty_success_rates.csv`: success rate by memory system and task difficulty, with Wilson 95% confidence intervals.
- `tables/paired_bootstrap_comparisons.csv`: paired episode-level bootstrap comparisons between history conditions.
- `tables/effect_sizes.csv`: compact effect-size table for no-history, k0, k1, k3, k7, and degradation from k0 to k7.

## Primary Figures

- `figures/overall_plain_success_by_condition.{png,pdf}`: headline success-rate curve. This is the cleanest main-paper plot.
- `figures/per_family_plain_success_small_multiples.{png,pdf}`: per-family success curves for every memory system.
- `figures/framesamp_modul_family_heatmap.{png,pdf}`: strongest variant heatmap across families and history conditions.
- `figures/difficulty_plain_success.{png,pdf}`: success rate by difficulty.
- `figures/interference_drop_k0_to_k7.{png,pdf}`: how much each memory system drops as relevant history is pushed behind distractors.

## Supporting Figures

- `figures/memory_lift_vs_no_history.{png,pdf}`: lift over each variant's own no-history condition.
- `figures/k0_lift_ranking.{png,pdf}`: nearest-prior lift ranking.

The headline figures use plain success rates, not lift, because the no-history floor differs by checkpoint and memory-system implementation.
