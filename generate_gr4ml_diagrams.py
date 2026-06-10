"""
Generate GR4ML diagrams aligned with Session-3 lecture notation.

Notation mapping (from Session 3.pdf):
  Business View   : Actor (stick-figure), Strategic/Decision(D)/Question(Q) Goals
                    (ovals), Insight (doc-rectangle), Indicator (traffic-light box)
                    Arrows: desires, supports, answers, evaluates, generates
  Analytics View  : PredictionGoal (split-pill oval), Algorithm (oval),
                    Softgoal (cloud/scalloped), influence symbols ++/+/-/--
                    Arrows: achieves, ++ / + / - / --
  Data Prep View  : Entity (table), Operator (rectangle), PrepTask (double-line rect)
                    Arrows: solid data-flow, dashed input/output
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "diagrams")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── palette ─────────────────────────────────────────────────────────
C_GOAL     = "#1565C0"
C_SOFTGOAL = "#E65100"
C_TASK     = "#2E7D32"
C_INSIGHT  = "#6A1B9A"
C_ACTOR    = "#37474F"
C_RESOURCE = "#4E342E"
C_INDIC    = "#00695C"
C_ALGO     = "#1B5E20"
C_MERGE    = "#455A64"
C_BG       = "#FAFAFA"
ARROW_CLR  = "#424242"

FS_TITLE = 15
FS_NODE  = 9.5
FS_LABEL = 8.5


# ═══════════════════════════════════════════════════════════════════
#  SHAPE HELPERS
# ═══════════════════════════════════════════════════════════════════
def _box(ax, xy, w, h, txt, color, fs=FS_NODE, tc="white", rad=0.25,
         ls="-", lw=1.3):
    b = FancyBboxPatch((xy[0]-w/2, xy[1]-h/2), w, h,
                       boxstyle=f"round,pad=0.08,rounding_size={rad}",
                       fc=color, ec="black", lw=lw, ls=ls)
    ax.add_patch(b)
    ax.text(xy[0], xy[1], txt, fontsize=fs, ha="center", va="center",
            color=tc, fontweight="bold")


def _oval(ax, xy, w, h, txt, color, fs=FS_NODE, tc="white", ls="-",
          lw=1.3):
    e = mpatches.Ellipse(xy, w, h, fc=color, ec="black", lw=lw, ls=ls)
    ax.add_patch(e)
    ax.text(xy[0], xy[1], txt, fontsize=fs, ha="center", va="center",
            color=tc, fontweight="bold")


def _cloud(ax, xy, w, h, txt, color=C_SOFTGOAL, fs=FS_NODE):
    """Softgoal – dashed-border ellipse (cloud proxy)."""
    e = mpatches.Ellipse(xy, w, h, fc=color, ec="black", lw=1.4,
                         ls=(0, (4, 3)), alpha=0.92)
    ax.add_patch(e)
    ax.text(xy[0], xy[1], txt, fontsize=fs, ha="center", va="center",
            color="white", fontweight="bold")


def _edge_oval(cx, cy, w, h, tx, ty):
    """Point on ellipse(cx,cy,w,h) border closest toward (tx,ty)."""
    import math
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return (cx + w/2, cy)
    a, b = w/2, h/2
    angle = math.atan2(dy, dx)
    return (cx + a * math.cos(angle), cy + b * math.sin(angle))


def _edge_box(cx, cy, w, h, tx, ty, pad=0.08):
    """Point on rectangle(cx,cy,w,h) border closest toward (tx,ty)."""
    import math
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return (cx, cy + (h/2 + pad))
    hw, hh = w/2 + pad, h/2 + pad
    sx = hw / abs(dx) if dx != 0 else 1e9
    sy = hh / abs(dy) if dy != 0 else 1e9
    s = min(sx, sy)
    return (cx + dx * s, cy + dy * s)


def _arrow(ax, fr, to, label="", color=ARROW_CLR, lw=1.4, rad=0.0,
           fs=FS_LABEL, offset=(0, 0), ls="-", ha="center"):
    style = f"arc3,rad={rad}"
    ax.annotate("", xy=to, xytext=fr,
                arrowprops=dict(arrowstyle="->", color=color, lw=lw,
                                connectionstyle=style, linestyle=ls,
                                shrinkA=0, shrinkB=0))
    if label:
        mx = (fr[0]+to[0])/2 + offset[0]
        my = (fr[1]+to[1])/2 + offset[1]
        ax.text(mx, my, label, fontsize=fs, ha=ha, va="center",
                color=color, fontstyle="italic",
                bbox=dict(boxstyle="round,pad=0.15", fc="white",
                          ec="none", alpha=0.9))


# ═══════════════════════════════════════════════════════════════════
#  1.  BUSINESS  VIEW
# ═══════════════════════════════════════════════════════════════════
def business_view():
    fig, ax = plt.subplots(figsize=(20, 14))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 14)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(C_BG)
    ax.set_title("GR4ML  --  Business View\n"
                 "(Automated Loan Underwriting)",
                 fontsize=FS_TITLE, fontweight="bold", pad=20)

    # ── Row-1: Actors (far left) ────────────────────────────────
    _oval(ax, (2.2, 11.5), 2.8, 1.1,
          "Actor:\nCredit Officer", C_ACTOR, 9)
    _oval(ax, (2.2, 9.0), 2.8, 1.1,
          "Actor:\nLoan Applicant", C_ACTOR, 9)

    # ── Row-2: Strategic Goals ──────────────────────────────────
    _oval(ax, (7, 11.5), 3.6, 1.2,
          "Strategic Goal:\nMinimize Loan\nDefaults", C_GOAL, 8.5)
    _oval(ax, (7, 9.0), 3.6, 1.2,
          "Strategic Goal:\nAutomate\nUnderwriting", C_GOAL, 8.5)

    # ── Row-3: Decision Goal ────────────────────────────────────
    _oval(ax, (12, 10.25), 4.0, 1.3,
          "[D] Decision Goal:\nApprove / Deny / Flag", C_TASK, 8.5)

    # ── Row-4: Question Goal + Indicators ───────────────────────
    _oval(ax, (17.5, 11.5), 3.4, 1.3,
          "[Q] Question:\nCredit risk\nacceptable?", C_GOAL, 8)

    # Indicator – traffic-light style box
    _box(ax, (17.5, 8.5), 3.6, 1.6,
         "Indicators:\nDefault < 2.5%\nAuto-appr > 80%\nLatency < 150ms",
         C_INDIC, 7.5)
    # mini traffic lights
    for i, c in enumerate(["#4CAF50", "#FFC107", "#F44336"]):
        circ = mpatches.Circle((16.1 + i*0.35, 9.35), 0.12,
                               fc=c, ec="black", lw=0.6)
        ax.add_patch(circ)

    # ── Row-5: Insights (bottom-centre) ─────────────────────────
    ins_y = 5.5
    _box(ax, (4.5, ins_y), 3.4, 1.1,
         "Insight:\nDefault Probability\nScore", C_INSIGHT, 8.5)
    _box(ax, (10, ins_y), 3.4, 1.1,
         "Insight:\nRisk Tier\n(LOW / MED / HIGH)", C_INSIGHT, 8.5)
    _box(ax, (15.5, ins_y), 3.4, 1.1,
         "Insight:\nComputed\nNet Worth", C_INSIGHT, 8.5)

    # ── Row-6: Softgoals (bottom) ───────────────────────────────
    sg_y = 2.8
    _cloud(ax, (4.5, sg_y), 3.4, 1.1, "Softgoal:\nAccuracy")
    _cloud(ax, (10, sg_y), 3.4, 1.1, "Softgoal:\nPerformance")
    _cloud(ax, (15.5, sg_y), 3.4, 1.1, "Softgoal:\nExplainability")

    # ══════════ ARROWS (edge-to-edge) ══════════
    # Actors -> Strategic Goals  (desires)
    a1_out = _edge_oval(2.2, 11.5, 2.8, 1.1, 7, 11.5)
    sg1_in = _edge_oval(7, 11.5, 3.6, 1.2, 2.2, 11.5)
    _arrow(ax, a1_out, sg1_in, "desires")
    a2_out = _edge_oval(2.2, 9.0, 2.8, 1.1, 7, 9.0)
    sg2_in = _edge_oval(7, 9.0, 3.6, 1.2, 2.2, 9.0)
    _arrow(ax, a2_out, sg2_in, "desires")

    # Strategic Goals -> Decision Goal  (supports)
    sg1_out = _edge_oval(7, 11.5, 3.6, 1.2, 12, 10.25)
    dg_in1  = _edge_oval(12, 10.25, 4.0, 1.3, 7, 11.5)
    _arrow(ax, sg1_out, dg_in1, "supports", offset=(0, 0.35))
    sg2_out = _edge_oval(7, 9.0, 3.6, 1.2, 12, 10.25)
    dg_in2  = _edge_oval(12, 10.25, 4.0, 1.3, 7, 9.0)
    _arrow(ax, sg2_out, dg_in2, "supports", offset=(0, -0.35))

    # Decision Goal -> Question Goal  (refines)
    dg_out_q = _edge_oval(12, 10.25, 4.0, 1.3, 17.5, 11.5)
    qg_in    = _edge_oval(17.5, 11.5, 3.4, 1.3, 12, 10.25)
    _arrow(ax, dg_out_q, qg_in, "refines", offset=(0, 0.3))

    # Decision Goal -> Indicators  (evaluates)
    dg_out_i = _edge_oval(12, 10.25, 4.0, 1.3, 17.5, 8.5)
    ind_in   = _edge_box(17.5, 8.5, 3.6, 1.6, 12, 10.25)
    _arrow(ax, dg_out_i, ind_in, "evaluates", offset=(0, -0.35))

    # Decision Goal -> Insights  (generates)
    dg_out_i1 = _edge_oval(12, 10.25, 4.0, 1.3, 4.5, 5.5)
    ins1_in   = _edge_box(4.5, 5.5, 3.4, 1.1, 12, 10.25)
    _arrow(ax, dg_out_i1, ins1_in, "generates",
           rad=0.15, offset=(-1.2, 0.4))
    dg_out_i2 = _edge_oval(12, 10.25, 4.0, 1.3, 10, 5.5)
    ins2_in   = _edge_box(10, 5.5, 3.4, 1.1, 12, 10.25)
    _arrow(ax, dg_out_i2, ins2_in, "generates",
           offset=(0.6, 0.4))
    dg_out_i3 = _edge_oval(12, 10.25, 4.0, 1.3, 15.5, 5.5)
    ins3_in   = _edge_box(15.5, 5.5, 3.4, 1.1, 12, 10.25)
    _arrow(ax, dg_out_i3, ins3_in, "generates",
           rad=-0.15, offset=(0.8, 0.4))

    # Insights -> Softgoals  (contributes +)
    i1_out = _edge_box(4.5, 5.5, 3.4, 1.1, 4.5, 2.8)
    s1_in  = _edge_oval(4.5, 2.8, 3.4, 1.1, 4.5, 5.5)
    _arrow(ax, i1_out, s1_in, "+", offset=(0.4, 0))
    i2_out = _edge_box(10, 5.5, 3.4, 1.1, 10, 2.8)
    s2_in  = _edge_oval(10, 2.8, 3.4, 1.1, 10, 5.5)
    _arrow(ax, i2_out, s2_in, "+", offset=(0.4, 0))
    i3_out = _edge_box(15.5, 5.5, 3.4, 1.1, 15.5, 2.8)
    s3_in  = _edge_oval(15.5, 2.8, 3.4, 1.1, 15.5, 5.5)
    _arrow(ax, i3_out, s3_in, "+", offset=(0.4, 0))

    # Insights answer Question Goal  (answers – dashed)
    i2_out_q = _edge_box(10, 5.5, 3.4, 1.1, 17.5, 11.5)
    qg_in_a  = _edge_oval(17.5, 11.5, 3.4, 1.3, 10, 5.5)
    _arrow(ax, i2_out_q, qg_in_a, "answers",
           rad=-0.2, ls="--", offset=(1.2, 0.3))

    # ── Legend ──
    legend = [
        mpatches.Patch(fc=C_ACTOR,   ec="k", label="Actor"),
        mpatches.Patch(fc=C_GOAL,    ec="k", label="Goal / Question [Q]"),
        mpatches.Patch(fc=C_TASK,    ec="k", label="Decision Goal [D]"),
        mpatches.Patch(fc=C_INSIGHT, ec="k", label="Insight"),
        mpatches.Patch(fc=C_SOFTGOAL,ec="k", label="Softgoal"),
        mpatches.Patch(fc=C_INDIC,   ec="k", label="Indicator"),
    ]
    ax.legend(handles=legend, loc="lower left", fontsize=9,
              framealpha=0.9, title="GR4ML Legend", title_fontsize=10)

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "gr4ml_business_view.png"),
                dpi=180, bbox_inches="tight")
    plt.close(fig)
    print("[OK] Business View saved.")


# ═══════════════════════════════════════════════════════════════════
#  2.  ANALYTICS  DESIGN  VIEW
#     FIXED: Only RandomForest (actually implemented).
#     Softgoals: Accuracy, Performance, Explainability (Feature Importance),
#                Reliability (Pydantic)
# ═══════════════════════════════════════════════════════════════════
def analytics_design_view():
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(C_BG)
    ax.set_title("GR4ML  --  Analytics Design View\n"
                 "(Algorithm Selection & Quality Softgoals)",
                 fontsize=FS_TITLE, fontweight="bold", pad=20)

    # ── PredictionGoal (top) ────────────────────────────────────
    _oval(ax, (8, 10.2), 6.0, 1.4,
          "PredictionGoal:\nPredict Default Risk (Binary)", C_GOAL, 10)
    # horizontal split line inside the oval
    ax.plot([5.5, 10.5], [10.2, 10.2], color="white", lw=1, ls="--",
            alpha=0.5)

    # ── Single Algorithm oval (centre, row 2) ──────────────────
    _oval(ax, (8, 7.2), 5.2, 1.4,
          "Algorithm:\nRandom Forest Classifier\n(n=150, depth=10)", C_ALGO, 9.5)

    # ── Softgoals (row 3) — 4 softgoals ────────────────────────
    sg_y = 3.8
    positions = [2.2, 6.0, 10.0, 14.0]
    labels = [
        "Softgoal:\nAccuracy\n(90.7%)",
        "Softgoal:\nPerformance\n(< 150 ms)",
        "Softgoal:\nExplainability\n(Feature Importance)",
        "Softgoal:\nReliability\n(Pydantic)",
    ]
    for x, lbl in zip(positions, labels):
        _cloud(ax, (x, sg_y), 3.4, 1.3, lbl, C_SOFTGOAL, 8)

    # ── Insight (bottom) ────────────────────────────────────────
    _box(ax, (8, 1.4), 5.0, 1.0,
         "Insight:  Feature Importance Ranking", C_INSIGHT, 9)

    # ══════════ ARROWS ══════════
    # Algorithm -> PredictionGoal  (achieves)
    rf_out = _edge_oval(8, 7.2, 5.2, 1.4, 8, 10.2)
    pg_in  = _edge_oval(8, 10.2, 6.0, 1.4, 8, 7.2)
    _arrow(ax, rf_out, pg_in, "achieves", offset=(1.2, 0))

    # RF -> softgoals (influence links)
    # RF -> Accuracy (++)
    rf_s1 = _edge_oval(8, 7.2, 5.2, 1.4, 2.2, 3.8)
    sg1_in = _edge_oval(2.2, 3.8, 3.4, 1.3, 8, 7.2)
    _arrow(ax, rf_s1, sg1_in, "++", rad=0.1, offset=(-0.5, 0.3))

    # RF -> Performance (+)
    rf_s2 = _edge_oval(8, 7.2, 5.2, 1.4, 6.0, 3.8)
    sg2_in = _edge_oval(6.0, 3.8, 3.4, 1.3, 8, 7.2)
    _arrow(ax, rf_s2, sg2_in, "+", rad=0.05, offset=(-0.3, 0.3))

    # RF -> Explainability (++)
    rf_s3 = _edge_oval(8, 7.2, 5.2, 1.4, 10.0, 3.8)
    sg3_in = _edge_oval(10.0, 3.8, 3.4, 1.3, 8, 7.2)
    _arrow(ax, rf_s3, sg3_in, "++", rad=-0.05, offset=(0.3, 0.3))

    # RF -> Reliability (+)
    rf_s4 = _edge_oval(8, 7.2, 5.2, 1.4, 14.0, 3.8)
    sg4_in = _edge_oval(14.0, 3.8, 3.4, 1.3, 8, 7.2)
    _arrow(ax, rf_s4, sg4_in, "+", rad=-0.1, offset=(0.5, 0.3))

    # Explainability -> Insight  (generates)
    exp_out = _edge_oval(10.0, 3.8, 3.4, 1.3, 8, 1.4)
    ins_in  = _edge_box(8, 1.4, 5.0, 1.0, 10.0, 3.8)
    _arrow(ax, exp_out, ins_in, "generates", offset=(0.5, 0.25))

    # ── Legend ──
    legend = [
        mpatches.Patch(fc=C_GOAL,    ec="k", label="PredictionGoal"),
        mpatches.Patch(fc=C_ALGO,    ec="k", label="Algorithm"),
        mpatches.Patch(fc=C_SOFTGOAL,ec="k", label="Softgoal"),
        mpatches.Patch(fc=C_INSIGHT, ec="k", label="Insight"),
    ]
    ax.legend(handles=legend, loc="lower left", fontsize=9,
              framealpha=0.9, title="GR4ML Legend", title_fontsize=10)

    # influence key
    ax.text(12.5, 1.0, "Influence key:   ++  Make   |   +  Help   "
            "|   -  Hurt   |   --  Break",
            fontsize=8, ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.3", fc="#FFF3E0",
                      ec=C_SOFTGOAL, lw=1))

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "gr4ml_analytics_design_view.png"),
                dpi=180, bbox_inches="tight")
    plt.close(fig)
    print("[OK] Analytics Design View saved.")


# ═══════════════════════════════════════════════════════════════════
#  3.  DATA  PREPARATION  VIEW
#     FIXED: Matches actual prepare_data.py implementation.
#     Single CSV source (Loan.csv), 5 actual prep tasks:
#       1. Drop non-predictive columns (36 -> 30)
#       2. Remove redundant features via correlation (30 -> 27)
#       3. Remove low-importance features (27 -> 21)
#       4. Categorical encoding (dict mapping)
#       5. Feature engineering (LoanToIncomeRatio, SavingsToLoanRatio)
#     Output: pd.DataFrame [1, 22]
# ═══════════════════════════════════════════════════════════════════
def data_preparation_view():
    fig, ax = plt.subplots(figsize=(17, 20))
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 20)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(C_BG)
    ax.set_title("GR4ML  --  Data Preparation View\n"
                 "(Pipeline Flow with Data Quality Goals)",
                 fontsize=FS_TITLE, fontweight="bold", pad=22)

    pipe_x = 5.0          # pipeline centre
    sg_x   = 13.0         # softgoal column centre

    # y-positions  (top = high)
    y_src   = 18.0
    y_t1    = 15.5
    y_t2    = 13.2
    y_t3    = 10.9
    y_t4    = 8.6
    y_t5    = 6.3
    y_out   = 3.8

    # ── START banner ────────────────────────────────────────────
    ax.text(pipe_x, 19.2, "DATA  FLOW  START",
            fontsize=11, ha="center", va="center", fontweight="bold",
            color="#1565C0",
            bbox=dict(boxstyle="round,pad=0.3", fc="#E3F2FD",
                      ec="#1565C0", lw=1.5))
    ax.text(sg_x, 19.2, "DATA  QUALITY  GOALS",
            fontsize=11, ha="center", va="center", fontweight="bold",
            color="#E65100",
            bbox=dict(boxstyle="round,pad=0.3", fc="#FFF3E0",
                      ec="#E65100", lw=1.5))

    # ── Data Source (single CSV) ───────────────────────────────
    _box(ax, (pipe_x, y_src), 5.4, 1.3,
         "Data Source:\nKaggle Loan.csv\n(20,000 records, 36 features)",
         C_RESOURCE, 8.5)

    # ── Pipeline Tasks ─────────────────────────────────────────
    tasks = [
        (y_t1, "Prep Task 1:\nDrop Non-Predictive Columns\n(ApplicationDate, RiskScore, InterestRate)\n36 → 30 features"),
        (y_t2, "Prep Task 2:\nRemove Redundant Features\n(Correlation > 0.95: MonthlyIncome,\nExperience, TotalAssets)  30 → 27"),
        (y_t3, "Prep Task 3:\nRemove Low-Importance Features\n(importance < 0.005: MaritalStatus,\nHomeOwnership, etc.)  27 → 21"),
        (y_t4, "Prep Task 4:\nCategorical Encoding\n(Dict mapping: EmploymentStatus,\nEducationLevel, LoanPurpose)"),
        (y_t5, "Prep Task 5:\nFeature Engineering\n(LoanToIncomeRatio,\nSavingsToLoanRatio)  21 → 22 + target"),
    ]
    tw, th = 5.8, 1.4
    for y, lbl in tasks:
        _box(ax, (pipe_x, y), tw, th, lbl, C_TASK, 7.5)
        # double bottom line for "Data Preparation Task" notation
        ax.plot([pipe_x - tw/2 + 0.15, pipe_x + tw/2 - 0.15],
                [y - th/2 + 0.08, y - th/2 + 0.08],
                color="white", lw=1.2, alpha=0.7)

    # Sequential arrows: source -> t1 -> t2 -> ... -> t5
    # Source -> T1
    src_out = _edge_box(pipe_x, y_src, 5.4, 1.3, pipe_x, y_t1)
    t1_in = _edge_box(pipe_x, y_t1, tw, th, pipe_x, y_src)
    _arrow(ax, src_out, t1_in, "", lw=2.2, color="#1565C0")

    # T1 -> T2 -> T3 -> T4 -> T5
    task_ys = [y_t1, y_t2, y_t3, y_t4, y_t5]
    for i in range(len(task_ys) - 1):
        fr_pt = _edge_box(pipe_x, task_ys[i], tw, th, pipe_x, task_ys[i+1])
        to_pt = _edge_box(pipe_x, task_ys[i+1], tw, th, pipe_x, task_ys[i])
        _arrow(ax, fr_pt, to_pt, "", lw=2.2, color="#1565C0")

    # ── Output ─────────────────────────────────────────────────
    out_w, out_h = 5.4, 1.2
    _oval(ax, (pipe_x, y_out), out_w, out_h,
          "Output:\nloan_data_processed.csv\n(pd.DataFrame  [20000, 22+1])",
          C_INDIC, 8.5)
    last_out = _edge_box(pipe_x, y_t5, tw, th, pipe_x, y_out)
    out_in   = _edge_oval(pipe_x, y_out, out_w, out_h, pipe_x, y_t5)
    _arrow(ax, last_out, out_in, "", lw=2.2, color="#1565C0")

    ax.text(pipe_x, 2.6, "DATA  FLOW  END",
            fontsize=11, ha="center", va="center", fontweight="bold",
            color="#2E7D32",
            bbox=dict(boxstyle="round,pad=0.3", fc="#E8F5E9",
                      ec="#2E7D32", lw=1.5))

    # ── Quality Softgoals (right column) ───────────────────────
    softgoals = [
        (y_t1, "Quality Goal:\nRelevant Features\n(no noise)"),
        (y_t2, "Quality Goal:\nNo Multicollinearity\n(independent features)"),
        (y_t3, "Quality Goal:\nParsimonious Model\n(no redundancy)"),
        (y_t4, "Quality Goal:\nHomogeneous\nEncoding"),
        (y_t5, "Quality Goal:\nRich Feature\nRepresentation"),
    ]
    sg_rels = [
        "operationalizes",
        "++",
        "+",
        "operationalizes",
        "++",
    ]
    sg_w, sg_h = 3.8, 1.2
    for (y, txt), rel in zip(softgoals, sg_rels):
        _cloud(ax, (sg_x, y), sg_w, sg_h, txt, C_SOFTGOAL, 8)
        task_out = _edge_box(pipe_x, y, tw, th, sg_x, y)
        sg_in    = _edge_oval(sg_x, y, sg_w, sg_h, pipe_x, y)
        _arrow(ax, task_out, sg_in,
               rel, color="#BF360C", lw=1.3,
               offset=(0, 0.35), ls="--")

    # ── Legend ──────────────────────────────────────────────────
    legend = [
        mpatches.Patch(fc=C_RESOURCE, ec="k",
                       label="Data Source (start)"),
        mpatches.Patch(fc=C_TASK,     ec="k",
                       label="Data Prep Task"),
        mpatches.Patch(fc=C_SOFTGOAL, ec="k",
                       label="Data Quality Softgoal"),
        mpatches.Patch(fc=C_INDIC,    ec="k",
                       label="Output Dataset (end)"),
    ]
    ax.legend(handles=legend, loc="lower left", fontsize=9,
              framealpha=0.9, title="GR4ML Legend", title_fontsize=10)

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "gr4ml_data_prep_view.png"),
                dpi=180, bbox_inches="tight")
    plt.close(fig)
    print("[OK] Data Preparation View saved.")


# ═══════════════════════════════════════════════════════════════════
#  4.  SYSTEM  ARCHITECTURE  DIAGRAM
# ═══════════════════════════════════════════════════════════════════
def system_architecture():
    fig, ax = plt.subplots(figsize=(22, 18))
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 18)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(C_BG)
    ax.set_title("System Architecture Diagram\n"
                 "Loan Approval Risk Service  (Pipe-and-Filter + Microservice)",
                 fontsize=16, fontweight="bold", pad=22)

    # ── colours for layers ──
    C_CLIENT  = "#1565C0"
    C_PIPE    = "#2E7D32"
    C_ML      = "#E65100"
    C_CFG     = "#37474F"
    C_LOG     = "#546E7A"
    C_DATA    = "#4E342E"

    bw, bh = 4.2, 1.1

    # ════════════════════════════════════════════════════════════
    #  LAYER BACKGROUNDS
    # ════════════════════════════════════════════════════════════
    r1 = mpatches.FancyBboxPatch((0.3, 0.5), 5.4, 16.5,
            boxstyle="round,pad=0.2", fc="#E3F2FD", ec=C_CLIENT,
            lw=1.5, alpha=0.3)
    ax.add_patch(r1)
    ax.text(3.0, 17.3, "NON-ML  COMPONENTS", fontsize=10,
            ha="center", fontweight="bold", color=C_CLIENT)

    r2 = mpatches.FancyBboxPatch((6.0, 0.5), 9.5, 16.5,
            boxstyle="round,pad=0.2", fc="#E8F5E9", ec=C_PIPE,
            lw=1.5, alpha=0.3)
    ax.add_patch(r2)
    ax.text(10.75, 17.3, "FastAPI  INFERENCE  SERVICE  (Pipe-and-Filter)",
            fontsize=10, ha="center", fontweight="bold", color=C_PIPE)

    r3 = mpatches.FancyBboxPatch((15.8, 0.5), 5.9, 16.5,
            boxstyle="round,pad=0.2", fc="#FFF3E0", ec=C_ML,
            lw=1.5, alpha=0.3)
    ax.add_patch(r3)
    ax.text(18.75, 17.3, "ML  COMPONENTS", fontsize=10,
            ha="center", fontweight="bold", color=C_ML)

    # ════════════════════════════════════════════════════════════
    #  NON-ML COLUMN (left)
    # ════════════════════════════════════════════════════════════
    _box(ax, (3.0, 15.5), bw, bh,
         "API Clients\n(Swagger UI / Web Portal)", C_CLIENT, 8.5)
    _box(ax, (3.0, 12.5), bw, bh,
         "Config Management\nconfigs/config.yaml\napp/config.py", C_CFG, 8)
    _box(ax, (3.0, 9.5), bw, bh,
         "GET /health\nLiveness + Readiness\nCheck", C_CLIENT, 8.5)
    _box(ax, (3.0, 6.5), bw, bh,
         "Pydantic Schemas\napp/schemas.py\n20 validated fields", C_CFG, 8)
    _box(ax, (3.0, 3.0), bw, 1.3,
         "Structured JSON Logger\napp/logger.py\nJSON to stdout\n(latency, decision, features)",
         C_LOG, 7.5)

    # ════════════════════════════════════════════════════════════
    #  INFERENCE PIPELINE (centre)
    # ════════════════════════════════════════════════════════════
    pw, ph = 5.0, 1.2
    pipe_x = 10.75

    _box(ax, (pipe_x, 15.5), pw, bh,
         "POST /predict\napp/main.py\n(FastAPI Route)", C_PIPE, 8.5)

    f1_y = 13.0
    _box(ax, (pipe_x, f1_y), pw, ph,
         "Filter 1: validate_input()\napp/pipeline.py\n"
         "Business rules + Pydantic  (Robustness)", C_PIPE, 7.5)

    f2_y = 10.5
    _box(ax, (pipe_x, f2_y), pw, ph,
         "Filter 2: extract_features()\nFeature engineering\n"
         "LoanToIncomeRatio, SavingsToLoanRatio\nBuilds DataFrame [1, 22]",
         C_PIPE, 7.5)

    f3_y = 8.0
    _box(ax, (pipe_x, f3_y), pw, ph,
         "Filter 3: run_model()\nRandomForest.predict_proba()\n"
         "threshold = 0.50  (from config)", C_PIPE, 7.5)

    f4_y = 5.5
    _box(ax, (pipe_x, f4_y), pw, ph,
         "Filter 4: format_response()\nRisk tier: LOW/MED/HIGH\n"
         "LoanApprovalResult JSON", C_PIPE, 7.5)

    _box(ax, (pipe_x, 3.0), pw, bh,
         "JSON Response\n{is_approved, probability,\n"
         "risk_tier, net_worth, latency_ms}", C_PIPE, 7.5)

    # Pipeline vertical arrows
    pipe_nodes = [15.5, f1_y, f2_y, f3_y, f4_y, 3.0]
    pipe_heights = [bh, ph, ph, ph, ph, bh]
    for i in range(len(pipe_nodes) - 1):
        fr = _edge_box(pipe_x, pipe_nodes[i], pw, pipe_heights[i],
                       pipe_x, pipe_nodes[i+1])
        to = _edge_box(pipe_x, pipe_nodes[i+1], pw, pipe_heights[i+1],
                       pipe_x, pipe_nodes[i])
        _arrow(ax, fr, to, "", lw=2.5, color=C_PIPE)

    # "pipe" labels
    for i, y_mid in enumerate([(f1_y+f2_y)/2, (f2_y+f3_y)/2, (f3_y+f4_y)/2]):
        ax.text(pipe_x + 2.8, y_mid, "pipe", fontsize=7.5,
                ha="center", color=C_PIPE, fontstyle="italic",
                bbox=dict(boxstyle="round,pad=0.1", fc="white",
                          ec=C_PIPE, alpha=0.7, lw=0.8))

    # ════════════════════════════════════════════════════════════
    #  ML COLUMN (right)
    # ════════════════════════════════════════════════════════════
    ml_x = 18.75

    _box(ax, (ml_x, 15.5), bw, bh,
         "Raw Data\ndata/Loan.csv\n(Kaggle, 36 columns)", C_DATA, 8.5)
    _box(ax, (ml_x, 13.0), bw, ph,
         "Data Preparation\ndata/prepare_data.py\nDrop 14 cols, Encode\n"
         "Engineer 2 ratios -> 22 features", C_ML, 7.5)
    _box(ax, (ml_x, 10.5), bw, ph,
         "Model Training\ntraining/step1_notebook.py\nRandomForest(n=150,\n"
         "depth=10)  Acc: 90.7%", C_ML, 7.5)
    _box(ax, (ml_x, 8.0), bw, bh,
         "Model Artifact\napp/model.pkl\n(joblib serialized)", C_ML, 8.5)
    _box(ax, (ml_x, 5.5), bw, bh,
         "ModelStore\napp/main.py\nLoads model at startup\n"
         "via joblib.load()", C_ML, 7.5)

    # ML pipeline vertical arrows
    ml_nodes = [15.5, 13.0, 10.5, 8.0, 5.5]
    ml_heights = [bh, ph, ph, bh, bh]
    ml_labels = ["", "feeds", "trains", "saves"]
    for i in range(len(ml_nodes) - 1):
        fr = _edge_box(ml_x, ml_nodes[i], bw, ml_heights[i],
                       ml_x, ml_nodes[i+1])
        to = _edge_box(ml_x, ml_nodes[i+1], bw, ml_heights[i+1],
                       ml_x, ml_nodes[i])
        _arrow(ax, fr, to, ml_labels[i], lw=1.8, color=C_ML,
               offset=(0.7, 0))

    # ════════════════════════════════════════════════════════════
    #  CROSS-LAYER ARROWS
    # ════════════════════════════════════════════════════════════
    fr = _edge_box(3.0, 15.5, bw, bh, pipe_x, 15.5)
    to = _edge_box(pipe_x, 15.5, pw, bh, 3.0, 15.5)
    _arrow(ax, fr, to, "POST /predict", color=C_CLIENT, lw=1.3,
           ls="--", offset=(0, 0.3))

    fr = _edge_box(3.0, 12.5, bw, bh, pipe_x, f1_y)
    to = _edge_box(pipe_x, f1_y, pw, ph, 3.0, 12.5)
    _arrow(ax, fr, to, "injects settings", color=C_CFG, lw=1.2,
           ls="--", offset=(0, 0.3))

    fr = _edge_box(3.0, 9.5, bw, bh, pipe_x, f2_y)
    to = _edge_box(pipe_x, f2_y, pw, ph, 3.0, 9.5)
    _arrow(ax, fr, to, "monitors", color=C_CLIENT, lw=1.2,
           ls="--", offset=(0, 0.3))

    fr = _edge_box(3.0, 6.5, bw, bh, pipe_x, f4_y)
    to = _edge_box(pipe_x, f4_y, pw, ph, 3.0, 6.5)
    _arrow(ax, fr, to, "schema\nvalidation", color=C_CFG, lw=1.2,
           ls="--", offset=(0, 0.3))

    fr = _edge_box(pipe_x, 3.0, pw, bh, 3.0, 3.0)
    to = _edge_box(3.0, 3.0, bw, 1.3, pipe_x, 3.0)
    _arrow(ax, fr, to, "logs\ntransaction", color=C_LOG, lw=1.2,
           ls="--", offset=(0, 0.35))

    fr = _edge_box(ml_x, 5.5, bw, bh, pipe_x, f3_y)
    to = _edge_box(pipe_x, f3_y, pw, ph, ml_x, 5.5)
    _arrow(ax, fr, to, "loads\nmodel", color=C_ML, lw=1.3,
           ls="--", offset=(0, -0.35))

    # ════════════════════════════════════════════════════════════
    #  LEGEND
    # ════════════════════════════════════════════════════════════
    legend = [
        mpatches.Patch(fc="#E3F2FD", ec=C_CLIENT, lw=1.5,
                       label="Non-ML (API, Config, Logging)"),
        mpatches.Patch(fc="#E8F5E9", ec=C_PIPE, lw=1.5,
                       label="Inference Service (Pipe-and-Filter)"),
        mpatches.Patch(fc="#FFF3E0", ec=C_ML, lw=1.5,
                       label="ML Components (Data, Training, Model)"),
    ]
    ax.legend(handles=legend, loc="lower center", fontsize=9,
              framealpha=0.95, title="Architecture Layers",
              title_fontsize=10, ncol=3,
              bbox_to_anchor=(0.5, -0.01))

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "system_architecture.png"),
                dpi=180, bbox_inches="tight")
    plt.close(fig)
    print("[OK] System Architecture saved.")


# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    business_view()
    analytics_design_view()
    data_preparation_view()
    system_architecture()
    print("\nAll diagrams regenerated in:", OUTPUT_DIR)
