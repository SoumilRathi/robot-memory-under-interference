# RoboMME-Interference Protocol

RoboMME-Interference is a cross-session interference protocol built on RoboMME-style robot memory tasks. The public project title is "Benchmarking Robot Memory Under Interference"; this protocol name is used only to identify the concrete evaluation procedure.

## Core Question

Can a memory-augmented robot policy use a relevant prior session when unrelated prior sessions are inserted between that memory and the current query?

## Setup

Each rollout has:

1. a query episode where the robot acts,
2. a history buffer available at query start,
3. a memory condition defining what history is present.

The policy interface stays fixed. Only the external history buffer changes.

## History Conditions

- `no-history`: empty external history at query start.
- `k0`: relevant lesson session only.
- `k1`: relevant lesson session followed by 1 unrelated distractor session.
- `k3`: relevant lesson session followed by 3 unrelated distractor sessions.
- `k7`: relevant lesson session followed by 7 unrelated distractor sessions.

The `k` value measures how far the relevant session is pushed back by unrelated robot experience.

## Task Families

The benchmark uses nine structural RoboMME task families:

- MoveCube
- RouteStick
- VideoUnmask
- VideoUnmaskSwap
- VideoRepick
- VideoPlaceButton
- VideoPlaceOrder
- InsertPeg
- PatternLock

Each family contributes 50 test episodes.

## Systems Evaluated

Baseline:

- `pi05_baseline`

Perceptual memory variants:

- `perceptual-framesamp-modul`
- `perceptual-tokendrop-modul`
- `perceptual-framesamp-context`
- `perceptual-framesamp-expert`
- `perceptual-tokendrop-context`
- `perceptual-tokendrop-expert`

Recurrent memory variants:

- `recurrent-ttt-expert`
- `recurrent-ttt-context`

Symbolic/oracle-style variants are excluded from the headline grid because they rely on privileged or structured information rather than the same visual-history pathway.

## Distractor Rule

Distractor sessions come from different task families than the query family. This avoids constructing arbitrary contradictory priors within the same task family and measures interference from unrelated robot experience.

## Metrics

Primary metric:

- rollout success rate.

Uncertainty:

- Wilson 95% confidence intervals for success rates.
- paired episode-level bootstrap confidence intervals for condition differences.

Pairing unit:

- `(task family, episode)` within each evaluated system.

## Coverage

Final grid:

- 9 task families,
- 9 systems,
- 5 history conditions,
- 18,450 completed rollouts,
- 369 / 369 complete cells.

The canonical rollout file is [`results/canonical_rollouts.csv`](results/canonical_rollouts.csv).
