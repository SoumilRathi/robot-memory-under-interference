# RoboMME-Interference Protocol

RoboMME-Interference is a cross-session interference protocol built on [RoboMME](https://robomme.github.io/) (Dai et al., ICML 2026). It reuses RoboMME's tasks, π₀.₅ checkpoints, and released memory-augmented variants, and adds a controlled way to vary how far back a relevant memory sits. The public project is titled *Benchmarking Robot Memory Under Interference*; "RoboMME-Interference" names the evaluation procedure.

## Core question

Can a memory-augmented policy still use a relevant prior session once unrelated sessions are inserted between that memory and the current query?

## History conditions

Every rollout is one query episode in which the policy acts, plus an external history buffer fixed at query start. The policy interface is unchanged from RoboMME; only the buffer contents vary.

| Condition | History buffer at query start |
| --- | --- |
| `no-history` | empty |
| `k0` | the relevant lesson session only |
| `k1` | the lesson, then 1 unrelated distractor session |
| `k3` | the lesson, then 3 unrelated distractor sessions |
| `k7` | the lesson, then 7 unrelated distractor sessions |

The lesson is always first; *k* is how far unrelated experience pushes it back.

## Distractor construction

Each distractor is a fixed unit: 32 stored frames sampled at stride 8 from a 256-frame session of a *different* task family than the query. Drawing from other families adds unrelated experience rather than contradictory facts about the same task. The fixed per-distractor size keeps every *k* step a comparable unit of interference, and *k* is capped at 7 to stay near the history lengths the variants were trained on.

## Task families

Nine families, 50 test episodes each: MoveCube, RouteStick, VideoUnmask, VideoUnmaskSwap, VideoRepick, VideoPlaceButton, VideoPlaceOrder, InsertPeg, PatternLock.

## Systems

Nine systems: the `pi05_baseline` (π₀.₅, no memory) plus eight memory-augmented variants. Each variant pairs a memory **representation** with a **mechanism** for integrating that memory into the policy:

- Perceptual representation (`framesamp`, `tokendrop`) × integration (`context`, `modul`, `expert`): `perceptual-framesamp-{context,modul,expert}` and `perceptual-tokendrop-{context,modul,expert}`.
- Recurrent representation (`ttt`) × integration: `recurrent-ttt-context` and `recurrent-ttt-expert`.

Excluded from the grid: RoboMME's symbolic variant, which reads privileged subtask annotations instead of the visual history; and RMT and the TTT-Modulator variant, which have no released checkpoints.

## Metric

Rollout success rate, with Wilson 95% confidence intervals. Effects are reported as differences between conditions (e.g. `k0` minus `no-history`); at 450 episodes per cell the effects are large and the intervals do not overlap, so the comparisons stand without resampling.

## Coverage

9 families × 9 systems × 5 conditions, with `pi05_baseline` evaluated only under `no-history`: 369 cells of 50 episodes — **18,450 rollouts, 369 / 369 complete**. The canonical record is [`results/canonical_rollouts.csv`](../results/canonical_rollouts.csv).
