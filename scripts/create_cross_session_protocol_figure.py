#!/usr/bin/env python3
"""Create the benchmark schematic for RoboMME-Interference.

One clean row: the history buffer holds the relevant lesson followed by k
unrelated sessions; the policy then acts in the query episode. k in {0,1,3,7}
controls how far back the relevant memory sits (no-history = empty buffer).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# Output path is resolved relative to this file, so the script works from any CWD.
# The diagram is a website asset (the paper is hosted on arXiv, not in this repo).
OUT_DIR = Path(__file__).resolve().parent.parent / "assets"

INK = "#171717"
MUTED = "#5a5a5a"
ACCENT = "#234f7e"
ACCENT_FILL = "#e9f0f7"
GRAY = "#9a9a9a"
GRAY_FILL = "#f1f1ef"


def box(ax, x, y, w, h, label, edge, fill, textcolor=INK, fontsize=12, lw=1.6):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            linewidth=lw,
            edgecolor=edge,
            facecolor=fill,
        )
    )
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fontsize, color=textcolor)


def arrow(ax, x0, x1, y):
    ax.add_patch(
        FancyArrowPatch(
            (x0, y),
            (x1, y),
            arrowstyle="-|>",
            mutation_scale=16,
            linewidth=1.6,
            color=INK,
            shrinkA=2,
            shrinkB=2,
        )
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 3.1))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 3.1)
    ax.axis("off")

    yc = 1.6
    h = 1.05
    yb = yc - h / 2

    # Relevant lesson (the one session that matters).
    box(ax, 0.35, yb, 2.25, h, "Relevant\nlesson", ACCENT, ACCENT_FILL, textcolor=ACCENT)

    # Unrelated sessions: offset shadows imply "x k".
    dx, dw = 3.45, 2.25
    for off in (0.26, 0.13):
        ax.add_patch(
            FancyBboxPatch(
                (dx + off, yb + off),
                dw,
                h,
                boxstyle="round,pad=0.02,rounding_size=0.06",
                linewidth=1.2,
                edgecolor=GRAY,
                facecolor=GRAY_FILL,
                alpha=0.55,
            )
        )
    box(ax, dx, yb, dw, h, "Unrelated\nsession", GRAY, "#ffffff", textcolor=MUTED)
    ax.text(dx + dw + 0.42, yb + 0.18, r"$\times\,k$", ha="left", va="center", fontsize=14, color=MUTED)

    # Query episode (where the policy acts).
    qx, qw = 7.85, 2.45
    box(ax, qx, yb, qw, h, "Query\nepisode", ACCENT, "#ffffff")

    # Flow arrows.
    arrow(ax, 2.6, 3.4, yc)
    arrow(ax, dx + dw + 0.85, qx - 0.05, yc)

    # Underbrace marking the history buffer (lesson + distractors).
    bx0, bx1 = 0.35, dx + dw + 0.7
    ybr = yb - 0.26
    ax.plot([bx0, bx1], [ybr, ybr], color=MUTED, lw=1.0)
    ax.plot([bx0, bx0], [ybr, ybr + 0.12], color=MUTED, lw=1.0)
    ax.plot([bx1, bx1], [ybr, ybr + 0.12], color=MUTED, lw=1.0)
    ax.text((bx0 + bx1) / 2, ybr - 0.2, "history buffer (memory)", ha="center", va="top", fontsize=11, color=MUTED)

    # Single k annotation.
    ax.text(
        0.35,
        0.32,
        r"$k \in \{0,1,3,7\}$ unrelated sessions sit between the lesson and the query"
        "        no-history: empty buffer",
        ha="left",
        va="center",
        fontsize=10.5,
        color=INK,
    )

    fig.savefig(OUT_DIR / "protocol_diagram.png", bbox_inches="tight", dpi=240)
    plt.close(fig)


if __name__ == "__main__":
    main()
