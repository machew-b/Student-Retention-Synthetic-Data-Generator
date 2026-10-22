"""
Figure 2 -- Latent and observed causal structure (PGM / DAG) of the generative
model, SD-193 whitepaper.

Rebuilt with matplotlib. Edit the CONFIG section: node positions/sizes, labels,
colours, and the EDGES list (each edge is a cubic Bezier you can reshape).

Coordinates are "canvas pixels": origin top-left, x right, y DOWN,
canvas 1050 x 1153 (same aspect ratio as the 2400 x 2635 PNG in the paper).

Run:   python fig2_dag.py            -> figures/fig2_dag.png (+ .pdf, .svg)
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse, Rectangle
from matplotlib.path import Path

# ----------------------------------------------------------------- CONFIG ---
W, H = 1050, 1153
FIG_W_IN = 8.0
DPI = 300
OUT_DIR = "figures"
OUT_NAME = "fig2_dag"

EDGE = "#333333"
DARK = "#222222"
RED = "#8b1a1a"
TXT_GREY = "#444444"

# Phase colour-coding (same as Fig. 1)
C_OBS = "#dbe8f5"     # Phase 3 observables (exported random variables)
C_INT = "#fbe7d1"     # Phase 4 risk score / intervention
C_OUT = "#f6d6d9"     # Phase 5 hazard / dropout
C_LAT = "white"       # latent (never exported)

FS = 7.6              # node text
FS_NOTE = 8.2         # plate captions
FS_LEGEND = 8

# Ellipse nodes: key -> (cx, cy, width, height, fill, dashed?, linewidth, text, bold?)
ELLIPSES = {
    "region":  (177, 89, 145, 50, C_OBS, False, 1.8, "Region Tier\n(High / Typical)", False),
    "income":  (391, 89, 111, 50, C_OBS, False, 1.8, "Income\nBracket", False),
    "work":    (570, 89, 142, 50, C_OBS, False, 1.8, "Working-Student\nStatus", False),
    "vuln":    (374, 192, 205, 58, C_LAT, True, 1.8, "Baseline\nVulnerability\n(latent, fixed at entry)", False),
    "shock0":  (212, 294, 154, 48, C_LAT, True, 1.8, "Term Shock t-1\n(latent)", False),
    "shock1":  (758, 294, 154, 48, C_LAT, True, 1.8, "Term Shock t\n(latent)", False),
    "grade0":  (126, 390, 111, 45, C_OBS, False, 1.8, "Term Grade", False),
    "att0":    (263, 390, 112, 45, C_OBS, False, 1.8, "Attendance\nRate", False),
    "hold0":   (400, 390, 111, 45, C_OBS, False, 1.8, "Financial\nHold", False),
    "grade1":  (604, 390, 111, 45, C_OBS, False, 1.8, "Term Grade", False),
    "att1":    (741, 390, 112, 45, C_OBS, False, 1.8, "Attendance\nRate", False),
    "hold1":   (878, 390, 111, 45, C_OBS, False, 1.8, "Financial\nHold", False),
    "interv":  (519, 596, 222, 62, C_INT, False, 1.8, "Support Intervention\n(term t)\nBernoulli(risk score)", False),
    "dropout": (519, 831, 257, 66, C_OUT, False, 2.6, "Dropout in Term t\n(target variable)\nBernoulli(h_(i,t))", True),
}

# Rectangle nodes (deterministic functions): key -> (x0, y0, x1, y1, fill, text)
RECTS = {
    "risk":   (391, 460, 647, 541, C_INT,
               "Observed Risk Score\n(term t)\nEq. 1: det. fn of\n(grade,att,hold)_(t-1)"),
    "hazard": (374, 662, 664, 750, C_OUT,
               "Dropout Hazard h_(i,t)\n(term t)\nEq. 3: det. fn of\n(vuln, shock_t, intervention_t)"),
}

# Plates
OUTER_PLATE = (28, 19, 1028, 969)           # student i = 1..N
INNER_PLATE = (54, 269, 1002, 947)          # term t = 1..T_i  (light grey fill)

# Plate captions / notes: (x, y, text, ha, fontsize, colour, style)
TEXTS = [
    (993, 59, "student i = 1,...,N\n(N=50,000)", "right", FS_NOTE + 1.5, TXT_GREY, "italic"),
    (967, 911, "term t = 1,...,T_i (T_i <= 8)\n[shown once: t-1 -> t]", "right", FS_NOTE + 1.5, TXT_GREY, "italic"),
    (725, 637, "\u221230% relative\nhazard reduction\nin any term with\nan intervention", "left", 7.6, RED, "italic"),
]

# ----- Edges -----------------------------------------------------------------
# Each edge: (list of points, colour, linewidth, z)
#   2 points  -> straight line
#   3 points  -> quadratic Bezier (start, control, end)
#   4 points  -> cubic Bezier (start, c1, c2, end)
# The arrowhead is drawn at the LAST point. Edit the control points to reshape.
BLACK = DARK
EDGES = [
    # exogenous -> baseline vulnerability
    ([(189, 120), (301, 163)], BLACK, 1.9, 4),
    ([(386, 127), (380, 150)], BLACK, 1.9, 4),
    ([(560, 121), (464, 163)], BLACK, 1.9, 4),
    # vulnerability -> shocks' neighbourhood (drawn to the shock ellipses)
    ([(365, 229), (330, 255), (243, 268)], BLACK, 1.6, 4),
    ([(385, 227), (520, 290), (730, 270)], BLACK, 1.6, 4),
    # vulnerability -> term t-1 observables
    ([(367, 236), (330, 330), (158, 364)], BLACK, 1.6, 4),
    ([(369, 238), (350, 300), (275, 353)], BLACK, 1.6, 4),
    ([(370, 238), (360, 290), (375, 354)], BLACK, 1.6, 4),
    # vulnerability -> term t observables
    ([(381, 236), (440, 360), (575, 364)], BLACK, 1.6, 4),
    ([(383, 236), (440, 330), (730, 365)], BLACK, 1.6, 4),
    # vulnerability -> hazard (passes behind the risk score box)
    ([(381, 236), (500, 340), (470, 540), (423, 652)], "#333333", 1.6, 2),
    # shock t -> hazard (passes behind the risk score box)
    ([(722, 317), (600, 400), (560, 560), (584, 643)], "#333333", 1.6, 2),
    # shock t-1 -> its observables
    ([(180, 318), (137, 354)], BLACK, 1.6, 4),
    ([(230, 318), (256, 352)], BLACK, 1.6, 4),
    ([(276, 311), (330, 330), (388, 357)], BLACK, 1.6, 4),
    # shock t -> its observables
    ([(718, 317), (618, 360)], BLACK, 1.6, 4),
    ([(752, 319), (746, 350)], BLACK, 1.6, 4),
    ([(788, 316), (864, 360)], BLACK, 1.6, 4),
    # PRIOR-TERM-ONLY dependencies (red): term t-1 observables -> risk score
    ([(165, 405), (260, 445), (400, 459)], RED, 1.9, 4),
    ([(296, 408), (360, 435), (425, 459)], RED, 1.9, 4),
    ([(411, 413), (428, 436), (441, 459)], RED, 1.9, 4),
    # risk score -> intervention -> hazard -> dropout
    ([(519, 541), (519, 550)], BLACK, 1.9, 4),
    ([(519, 626), (519, 651)], BLACK, 1.9, 4),
    ([(519, 750), (519, 782)], BLACK, 2.6, 4),
]

# small boxed label on the red edges
PRIOR_LABEL = (357, 431, "prior term\nonly")

# Legend (bottom-left): box + rows (y, kind, label)
LEGEND_BOX = (14, 999, 372, 1134)
LEGEND_X0, LEGEND_X1 = 22, 44
LEGEND = [
    (1013, "rect_obs", "Random variable, observed (exported)"),
    (1035, "rect_lat", "Random variable, latent (never exported)"),
    (1056, "rect_det", "Deterministic function, observed"),
    (1077, "line_black", "Causal / generative dependency"),
    (1098, "line_red", "Prior-term-only dependency"),
    (1119, "plate", "Plate: repeated structure (index at corner)"),
]
# ------------------------------------------------------------- END CONFIG ---


def bezier_path(pts):
    n = len(pts)
    if n == 2:
        return Path(pts, [Path.MOVETO, Path.LINETO])
    if n == 3:
        return Path(pts, [Path.MOVETO, Path.CURVE3, Path.CURVE3])
    if n == 4:
        return Path(pts, [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
    raise ValueError("an edge needs 2, 3 or 4 points")


def build():
    fig = plt.figure(figsize=(FIG_W_IN, FIG_W_IN * H / W), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")

    def rbox(x0, y0, x1, y1, fc="none", ec=EDGE, lw=2.0, ls="-", r=24, z=1):
        ax.add_patch(FancyBboxPatch((x0 + r, y0 + r), (x1 - x0) - 2 * r, (y1 - y0) - 2 * r,
                                    boxstyle=f"round,pad={r}", fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))

    # plates
    rbox(*OUTER_PLATE, ec="#555555", lw=2.0, ls=(0, (5, 3)), r=26, z=0.5)
    rbox(*INNER_PLATE, fc="#fbfbfb", ec="#555555", lw=1.5, ls=(0, (5, 3)), r=26, z=0.6)

    # edges first (so nodes sit on top where intended)
    for (pts, col, lw, z) in EDGES:
        ax.add_patch(FancyArrowPatch(path=bezier_path(pts), arrowstyle="-|>", mutation_scale=11,
                                     lw=lw, color=col, shrinkA=0, shrinkB=0, zorder=z))

    # ellipse nodes
    for key, (cx, cy, w, h, fc, dashed, lw, txt, bold) in ELLIPSES.items():
        ax.add_patch(Ellipse((cx, cy), w, h, fc=fc, ec=EDGE, lw=lw,
                             ls=(0, (3.5, 2.5)) if dashed else "-", zorder=5))
        ax.text(cx, cy, txt, ha="center", va="center", fontsize=FS, zorder=6,
                fontweight="bold" if bold else "normal", linespacing=1.1)

    # rectangle nodes
    for key, (x0, y0, x1, y1, fc, txt) in RECTS.items():
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=fc, ec=EDGE, lw=1.8, zorder=5))
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, txt, ha="center", va="center",
                fontsize=FS, zorder=6, linespacing=1.1)

    # free text
    for (x, y, t, ha, fs, col, st) in TEXTS:
        ax.text(x, y, t, ha=ha, va="center", fontsize=fs, color=col, style=st,
                zorder=6, linespacing=1.1)

    # "prior term only" tag
    px, py, ptxt = PRIOR_LABEL
    ax.text(px, py, ptxt, ha="center", va="center", fontsize=7, color=RED, style="italic",
            zorder=8, linespacing=1.05,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=RED, lw=0.8))

    # legend
    ax.add_patch(FancyBboxPatch((LEGEND_BOX[0] + 4, LEGEND_BOX[1] + 4),
                                LEGEND_BOX[2] - LEGEND_BOX[0] - 8, LEGEND_BOX[3] - LEGEND_BOX[1] - 8,
                                boxstyle="round,pad=4", fc="white", ec="#cccccc", lw=1.0, zorder=3))
    for (y, kind, label) in LEGEND:
        x0, x1 = LEGEND_X0, LEGEND_X1
        if kind == "rect_obs":
            ax.add_patch(Rectangle((x0, y - 5), x1 - x0, 10, fc=C_OBS, ec=EDGE, lw=1.2, zorder=4))
        elif kind == "rect_lat":
            ax.add_patch(Rectangle((x0, y - 5), x1 - x0, 10, fc="white", ec=EDGE, lw=1.2,
                                   ls=(0, (2.5, 1.5)), zorder=4))
        elif kind == "rect_det":
            ax.add_patch(Rectangle((x0, y - 5), x1 - x0, 10, fc=C_INT, ec=EDGE, lw=1.2, zorder=4))
        elif kind == "line_black":
            ax.plot([x0, x1], [y, y], color="#333333", lw=2.0, zorder=4)
        elif kind == "line_red":
            ax.plot([x0, x1], [y, y], color=RED, lw=2.0, zorder=4)
        else:
            ax.add_patch(Rectangle((x0, y - 5), x1 - x0, 10, fc="none", ec="#555555", lw=1.2,
                                   ls=(0, (3, 2)), zorder=4))
        ax.text(x1 + 12, y, label, va="center", ha="left", fontsize=FS_LEGEND, zorder=4)
    return fig


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    fig = build()
    for ext in ("png", "pdf", "svg"):
        fig.savefig(os.path.join(OUT_DIR, f"{OUT_NAME}.{ext}"), dpi=DPI, facecolor="white")
    print("saved", os.path.join(OUT_DIR, OUT_NAME + ".png"))
