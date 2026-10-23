"""
Figure 1 -- End-to-end synthetic cohort generation pipeline (SD-193 whitepaper).

Rebuilt with matplotlib. Everything you are likely to edit is in the CONFIG
section: box positions/sizes, colours, text, fonts and arrows.

Coordinates are in "canvas pixels": origin top-left, x to the right, y DOWN,
canvas 1300 x 919 (same aspect ratio as the 2658 x 1880 PNG in the paper).

Run:   python fig1_pipeline.py            -> figures/fig1_pipeline.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ----------------------------------------------------------------- CONFIG ---
W, H = 1300, 919                 # canvas size (px units)
FIG_W_IN = 8.86                  # figure width in inches (height follows W:H)
DPI = 300
OUT_DIR = "figures"
OUT_NAME = "fig1_pipeline"

EDGE = "#333333"
DARK = "#222222"
GREY = "#707070"
RED = "#8b1a1a"
TXT_GREY = "#444444"

FS_BOX = 12      # text inside phase boxes
FS_LABEL = 10      # red italic annotation labels
FS_SMALL = 8.5     # small red labels
FS_NOTE = 10.5     # grey italic notes
FS_LEGEND = 11

# Phase boxes: key -> (x0, y0, x1, y1, fill colour, text)
BOXES = {
    "p1":  (87, 158, 349, 301, "#e8e8e8", "Phase 1\nCohort & Region\nInitialization"),
    "p2":  (87, 308, 349, 414, "#e4dcf3", "Phase 2\nLatent State\nAssignment"),
    "p3":  (442, 158, 666, 301, "#dbe8f5", "Phase 3\nTerm-by-Term\nObservable Gen."),
    "p4":  (693, 158, 917, 301, "#fbe7d1", "Phase 4\nConfounded\nIntervention"),
    "p5a": (944, 158, 1168, 301, "#f6d6d9", "Phase 5a\nOutcome Gen.\n(per-term draw)"),
    "p5b": (277, 588, 1021, 798, "#d9ecd8",
            "Phase 5b: Batch Validation (cohort-level)\nRuns once the full synthetic cohort\n"
            "exists; checks aggregate outcomes\nagainst Table 4 benchmarks"),
}

# Plates (dashed rounded rectangles): (x0, y0, x1, y1, linewidth)
OUTER_PLATE = (38, 98, 1270, 463, 2.0)
INNER_PLATE = (398, 157, 1202, 422, 1.5)

# Free text: (x, y, text, ha, fontsize, colour, style)
TEXTS = [
    (1236, 45, "student i = 1,...,N\n(N=50,000)", "right", FS_NOTE + 1, TXT_GREY, "italic"),
    (204, 133, "region tier, income\nbracket, work status", "center", FS_LABEL, RED, "italic"),
    (672, 133, "grade, attendance,\nhold (term t-1 & t)", "center", FS_LABEL, RED, "italic"),
    (923, 133, "risk score,\nintervention flag", "center", FS_LABEL, RED, "italic"),
    (1188, 385, "term t = 1,...,T_i\n(T_i \u2264 8)", "right", FS_NOTE + 1, TXT_GREY, "italic"),
    (478, 441, "baseline vuln. (fixed);\nshock (redrawn/term)", "center", FS_SMALL, RED, "italic"),
    (1094, 493, "full cohort of\nper-term outcomes", "center", FS_NOTE + 1, "#333333", "italic"),
    (125, 607, "feedback: simulated\nvs. real cohort-level\nattrition (Table 4) ->\nrevised Phase 1/2\nparameters",
     "center", FS_NOTE, "#555555", "italic"),
]

# Arrows: (start (x,y), end (x,y), connection rad, colour, linewidth, linestyle)
# rad = curvature (0 = straight). Flip its sign to bend the other way.
ARROWS = [
    ((349, 229), (442, 229), 0.0, DARK, 1.8, "-"),       # P1 -> P3
    ((218, 301), (218, 308), 0.0, DARK, 1.2, "-"),       # P1 -> P2 (short)
    ((349, 358), (442, 262), 0.25, DARK, 1.8, "-"),      # P2 -> P3
    ((666, 229), (693, 229), 0.0, DARK, 1.8, "-"),       # P3 -> P4
    ((917, 229), (944, 229), 0.0, DARK, 1.8, "-"),       # P4 -> P5a
    ((1055, 301), (780, 588), -0.22, DARK, 1.8, "-"),    # P5a -> P5b
    ((277, 660), (105, 414), 0.22, GREY, 1.8, (0, (4, 2.5))),  # feedback loop (dashed)
]

# Legend rows: (y, kind, label)  -- drawn bottom-left
LEGEND_X = 33
LEGEND = [
    (836, "arrow", "per-student / per-term data flow"),
    (866, "dash", "cohort-level feedback (calibration loop)"),
    (898, "plate", "plate: repeated structure (index at corner)"),
]
# ------------------------------------------------------------- END CONFIG ---


def build():
    fig = plt.figure(figsize=(FIG_W_IN, FIG_W_IN * H / W), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)            # y grows downward
    ax.axis("off")

    def rbox(x0, y0, x1, y1, fc="none", ec=EDGE, lw=2.0, ls="-", r=22, z=2):
        p = FancyBboxPatch((x0 + r, y0 + r), (x1 - x0) - 2 * r, (y1 - y0) - 2 * r,
                           boxstyle=f"round,pad={r}", fc=fc, ec=ec, lw=lw, ls=ls, zorder=z)
        ax.add_patch(p)

    # plates
    for (x0, y0, x1, y1, lw) in (OUTER_PLATE, INNER_PLATE):
        rbox(x0, y0, x1, y1, ec="#555555", lw=lw, ls=(0, (5, 3)), r=26 if lw > 1.8 else 22, z=1)

    # phase boxes
    for key, (x0, y0, x1, y1, fc, txt) in BOXES.items():
        rbox(x0, y0, x1, y1, fc=fc, lw=1.6)
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, txt, ha="center", va="center",
                fontsize=FS_BOX, color="black", zorder=5, linespacing=1.15)

    # annotation text
    for (x, y, t, ha, fs, col, st) in TEXTS:
        ax.text(x, y, t, ha=ha, va="center", fontsize=fs, color=col, style=st,
                zorder=5, linespacing=1.1)

    # arrows
    for (a, b, rad, col, lw, ls) in ARROWS:
        ax.add_patch(FancyArrowPatch(a, b, connectionstyle=f"arc3,rad={rad}",
                                     arrowstyle="-|>", mutation_scale=13, lw=lw,
                                     color=col, linestyle=ls, shrinkA=0, shrinkB=0, zorder=4))

    # legend
    for (y, kind, label) in LEGEND:
        x0, x1 = LEGEND_X, LEGEND_X + 43
        if kind == "arrow":
            ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>", mutation_scale=14,
                                         lw=1.6, color=DARK, shrinkA=0, shrinkB=0))
        elif kind == "dash":
            ax.plot([x0, x1], [y, y], color=GREY, lw=1.8, ls=(0, (3, 2)))
        else:
            rbox(x0, y - 8, x1 - 8, y + 8, ec="#555555", lw=1.2, ls=(0, (4, 2)), r=4)
        ax.text(x1 + 17, y, label, va="center", ha="left", fontsize=FS_LEGEND, color="black")
    return fig


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    fig = build()
    output_path = os.path.join(OUT_DIR, OUT_NAME + ".png")
    fig.savefig(output_path, dpi=DPI, facecolor="white")
    print("saved", output_path)
