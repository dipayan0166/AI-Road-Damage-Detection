"""
Asphalt Ochre (dark) theme for the Smart Road Damage Detection & Inspection System.

Drop this file next to your main Streamlit file, put config.toml in .streamlit/,
then in the main file (and in every page file if you use a pages/ folder):

    import streamlit as st
    st.set_page_config(page_title="Road Damage Inspection", page_icon="🛣️", layout="wide")

    from theme import apply_theme
    apply_theme()                 # CSS + matplotlib style. Call right after set_page_config.

Helpers you can use on the pages:

    kpi_grid([...])               # the five KPI cards on Home
    condition_banner(...)         # the Road Condition banner (Single Image Studio, Batch reports)
    draw_pie / draw_bars          # matplotlib charts in the theme
    LOSS_TRAIN / LOSS_VAL         # line styles for the training telemetry charts
    rating_cell_style             # colours the Rating column in tables

Fonts (Inter for text, Newsreader for headings) load from Google Fonts, so the
machine running the app needs internet access once.
"""

from __future__ import annotations

import html

# --------------------------------------------------------------------------
# Design tokens
# --------------------------------------------------------------------------
PALETTE = {
    "bg": "#121315",          # page
    "side": "#0E0F11",        # sidebar
    "card": "#191A1D",        # cards, inputs, chart background
    "border": "#26282D",
    "navactive": "#23262B",   # active sidebar page, hover
    "text": "#ECEDEF",
    "muted": "#9EA2AB",
    "accent": "#D2A24C",      # ochre
    "accent_ink": "#1B1405",  # text on an ochre button
    "grid": "#212328",
    # semantic: solid / tinted background / readable text on the tint
    "good": "#6FBF8E", "good_bg": "rgba(111,191,142,0.14)", "good_fg": "#8FD3AA",
    "fair": "#E0B04F", "fair_bg": "rgba(224,176,79,0.14)", "fair_fg": "#EBC677",
    "poor": "#E8905A", "poor_bg": "rgba(232,144,90,0.14)", "poor_fg": "#F2AE82",
    "crit": "#E5736A", "crit_bg": "rgba(229,115,106,0.14)", "crit_fg": "#F09A92",
    # categorical chart colours: Pothole, Alligator, Transverse, Longitudinal
    "c1": "#6FA0D6", "c2": "#E5736A", "c3": "#E0B04F", "c4": "#5CB8A8",
}

CATEGORICAL = [PALETTE["c1"], PALETTE["c2"], PALETTE["c3"], PALETTE["c4"]]

# Severity bars (Minor / Moderate / Critical)
SEVERITY_COLORS = {"Minor": PALETTE["good"], "Moderate": PALETTE["fair"], "Critical": PALETTE["crit"]}

# Rating -> tone name used by kpi_card / condition_banner
RATING_TONE = {"GOOD": "good", "FAIR": "fair", "POOR": "poor", "CRITICAL": "crit"}

# Training telemetry chart styles
LOSS_TRAIN = dict(color=PALETTE["c1"], linewidth=1.7)
LOSS_VAL = dict(color=PALETTE["fair"], linewidth=1.7, linestyle="--")

FONT_BODY = "Inter, system-ui, sans-serif"
FONT_HEAD = "Newsreader, Georgia, serif"


def tone_for_rating(rating: str) -> str:
    """'Fair' / 'FAIR' / 'fair ' -> 'fair'. Unknown ratings fall back to 'fair'."""
    return RATING_TONE.get(str(rating).strip().upper(), "fair")


def rating_cell_style(value) -> str:
    """For df.style.map(rating_cell_style, subset=['rating']) - colours the rating text."""
    tone = tone_for_rating(value)
    return f"color: {PALETTE[tone + '_fg']}; font-weight: 600"


# --------------------------------------------------------------------------
# CSS
# --------------------------------------------------------------------------
def _css_vars() -> str:
    p = PALETTE
    pairs = {
        "bg": p["bg"], "side": p["side"], "card": p["card"], "border": p["border"],
        "navactive": p["navactive"], "text": p["text"], "muted": p["muted"],
        "accent": p["accent"], "accent-ink": p["accent_ink"], "grid": p["grid"],
        "radius": "8px", "shadow": "0 1px 0 rgba(255,255,255,0.02)",
        "font-body": FONT_BODY, "font-head": FONT_HEAD,
    }
    for tone in ("good", "fair", "poor", "crit"):
        pairs[tone] = p[tone]
        pairs[tone + "-bg"] = p[tone + "_bg"]
        pairs[tone + "-fg"] = p[tone + "_fg"]
    for i in range(1, 5):
        pairs[f"c{i}"] = p[f"c{i}"]
    return ":root{" + ";".join(f"--{k}:{v}" for k, v in pairs.items()) + "}"


_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:wght@500;600&display=swap');

/* ---------- page + typography ---------- */
.stApp, [data-testid="stAppViewContainer"] { background: var(--bg); color: var(--text); }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 3rem; padding-bottom: 3rem; max-width: 1400px; }

.stApp, .stApp p, .stApp li, .stApp label, .stApp button, .stApp input, .stApp textarea,
[data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"] *, [data-testid="stCaptionContainer"] {
  font-family: var(--font-body) !important;
}
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
  font-family: var(--font-head) !important;
  font-weight: 500 !important;
  letter-spacing: -0.01em;
  color: var(--text);
}
.stApp h1 { font-size: 2rem !important; letter-spacing: -0.015em; }
.stApp h2 { font-size: 1.375rem !important; }
.stApp h3 { font-size: 1.125rem !important; }
[data-testid="stCaptionContainer"], .stApp small { color: var(--muted) !important; }
hr { border-color: var(--border) !important; }

/* ---------- sidebar + page navigation ---------- */
[data-testid="stSidebar"] { background: var(--side); border-right: 1px solid var(--border); }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { font-size: 1.06rem !important; }
[data-testid="stSidebarNav"] a, [data-testid="stSidebarNavLink"] {
  padding: 8px 12px; border-radius: var(--radius); color: var(--muted) !important;
  font-size: 13px; text-decoration: none;
}
[data-testid="stSidebarNav"] a:hover, [data-testid="stSidebarNavLink"]:hover { background: var(--navactive); color: var(--text) !important; }
[data-testid="stSidebarNav"] a[aria-current="page"], [data-testid="stSidebarNavLink"][aria-current="page"] {
  background: var(--navactive); color: var(--text) !important; font-weight: 600;
}

/* ---------- tabs ---------- */
button[data-baseweb="tab"] { color: var(--muted); font-weight: 500; }
button[data-baseweb="tab"][aria-selected="true"] { color: var(--text); font-weight: 600; }
[data-baseweb="tab-highlight"] { background-color: var(--accent) !important; }
[data-baseweb="tab-border"] { background-color: var(--border) !important; }

/* ---------- st.metric cards ---------- */
[data-testid="stMetric"] {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 16px 18px; box-shadow: var(--shadow);
}
[data-testid="stMetricLabel"] p {
  color: var(--muted) !important; font-size: 0.7rem !important; font-weight: 500;
  text-transform: uppercase; letter-spacing: 0.08em;
}
[data-testid="stMetricValue"], [data-testid="stMetricValue"] * {
  font-family: var(--font-body) !important; font-weight: 500 !important; color: var(--text);
  font-size: 1.75rem !important; letter-spacing: -0.01em; font-variant-numeric: tabular-nums;
}
[data-testid="stMetricDelta"], [data-testid="stMetricDelta"] * { color: var(--good-fg) !important; fill: var(--good-fg) !important; }
[data-testid="stMetricDelta"] {
  background: var(--good-bg); border-radius: 4px; padding: 1px 8px; width: fit-content; font-size: 0.72rem;
}

/* ---------- buttons ---------- */
.stButton > button, [data-testid="stDownloadButton"] > button,
button[data-testid="stBaseButton-secondary"] {
  background: var(--card); color: var(--text); border: 1px solid var(--border);
  border-radius: var(--radius); font-weight: 500;
}
.stButton > button:hover, [data-testid="stDownloadButton"] > button:hover,
button[data-testid="stBaseButton-secondary"]:hover { border-color: var(--accent); color: var(--accent); }
.stButton > button[kind="primary"], button[data-testid="stBaseButton-primary"] {
  background: var(--accent); color: var(--accent-ink); border-color: var(--accent); font-weight: 600;
}
.stButton > button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover {
  background: var(--accent); color: var(--accent-ink); filter: brightness(1.08);
}

/* ---------- inputs ---------- */
[data-baseweb="select"] > div { background: var(--card) !important; border-color: var(--border) !important; border-radius: var(--radius); }
[data-testid="stSlider"] [role="slider"] { background-color: var(--accent) !important; }
[data-testid="stFileUploaderDropzone"] { background: var(--card); border: 1px dashed var(--border); border-radius: var(--radius); }
[data-testid="stFileUploaderFile"] { color: var(--text); }

/* ---------- progress bar ---------- */
[data-testid="stProgress"] [role="progressbar"] { background: var(--grid) !important; border-radius: 999px; }
[data-testid="stProgress"] [role="progressbar"] > div { background-color: var(--accent) !important; border-radius: 999px; }

/* ---------- alerts (info / success / warning / error) ---------- */
[data-testid="stAlert"] {
  background: var(--card); color: var(--text); border: 1px solid var(--border); border-radius: var(--radius);
}
[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) { background: var(--card); }
[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) svg { fill: var(--accent) !important; }
[data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) { background: var(--good-bg); }
[data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) svg { fill: var(--good) !important; }
[data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) { background: var(--fair-bg); }
[data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) svg { fill: var(--fair) !important; }
[data-testid="stAlert"]:has([data-testid="stAlertContentError"]) { background: var(--crit-bg); }
[data-testid="stAlert"]:has([data-testid="stAlertContentError"]) svg { fill: var(--crit) !important; }

/* ---------- expanders, images, tables ---------- */
[data-testid="stExpander"] details { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); }
[data-testid="stExpander"] summary { color: var(--text); font-weight: 500; }
[data-testid="stImage"] img, [data-testid="stImageContainer"] img { border-radius: var(--radius); border: 1px solid var(--border); }
[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }

/* ---------- custom HTML components from theme.py ---------- */
.rd-kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 16px; margin: 8px 0 24px; }
.rd-kpi {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  box-shadow: var(--shadow); padding: 16px 18px; display: flex; flex-direction: column; gap: 12px;
}
.rd-kpi__head { display: flex; align-items: center; gap: 8px; }
.rd-kpi__dot { width: 7px; height: 7px; border-radius: 50%; background: var(--accent); }
.rd-kpi__label { font-size: 11px; font-weight: 500; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; }
.rd-kpi__value { font-size: 28px; font-weight: 500; letter-spacing: -0.01em; color: var(--text); font-variant-numeric: tabular-nums; }
.rd-kpi__unit { font-size: 14px; font-weight: 400; color: var(--muted); }

.rd-banner {
  text-align: center; padding: 28px 24px; margin: 8px 0 24px; border-radius: var(--radius);
  border: 1px solid var(--border); background: var(--fair-bg); display: flex; flex-direction: column; gap: 10px;
}
.rd-banner__title { font-family: var(--font-head); font-size: 30px; font-weight: 500; letter-spacing: -0.01em; margin: 0; }
.rd-banner__msg { font-size: 15px; color: var(--text); margin: 0; }
.rd-banner__meta { font-size: 12px; color: var(--muted); margin: 0; }
.rd-banner--good { background: var(--good-bg); border-color: color-mix(in srgb, var(--good) 45%, var(--card)); }
.rd-banner--good .rd-banner__title { color: var(--good-fg); }
.rd-banner--fair { background: var(--fair-bg); border-color: color-mix(in srgb, var(--fair) 45%, var(--card)); }
.rd-banner--fair .rd-banner__title { color: var(--fair-fg); }
.rd-banner--poor { background: var(--poor-bg); border-color: color-mix(in srgb, var(--poor) 45%, var(--card)); }
.rd-banner--poor .rd-banner__title { color: var(--poor-fg); }
.rd-banner--crit { background: var(--crit-bg); border-color: color-mix(in srgb, var(--crit) 45%, var(--card)); }
.rd-banner--crit .rd-banner__title { color: var(--crit-fg); }
"""

_HIDE_CHROME_CSS = """
[data-testid="stToolbar"], [data-testid="stDecoration"], footer { visibility: hidden; height: 0; }
"""


def apply_theme(hide_chrome: bool = False, font_dir: str | None = None) -> None:
    """Inject the Asphalt Ochre CSS and configure matplotlib.

    Call once at the top of the main file and of every page file, directly after
    st.set_page_config(). hide_chrome=True hides the Deploy button / menu / footer.
    font_dir: optional folder with Inter .ttf files so matplotlib charts use Inter too.
    """
    import streamlit as st

    css = _css_vars() + _CSS + (_HIDE_CHROME_CSS if hide_chrome else "")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    apply_matplotlib_theme(font_dir=font_dir)


# --------------------------------------------------------------------------
# HTML helpers (use with st.markdown(..., unsafe_allow_html=True))
# --------------------------------------------------------------------------
def kpi_card(label: str, value, unit: str = "", tone: str = "accent") -> str:
    """One KPI card. tone: accent | c1 | good | fair | poor | crit."""
    return (
        '<div class="rd-kpi">'
        '<div class="rd-kpi__head">'
        f'<span class="rd-kpi__dot" style="background: var(--{html.escape(tone)})"></span>'
        f'<span class="rd-kpi__label">{html.escape(str(label))}</span>'
        "</div>"
        f'<div class="rd-kpi__value">{html.escape(str(value))}'
        f'<span class="rd-kpi__unit">{html.escape(str(unit))}</span></div>'
        "</div>"
    )


def kpi_grid(items) -> str:
    """items: list of (label, value, unit, tone) or dicts. Returns the HTML for the whole row.

        st.markdown(kpi_grid([
            ("Total Inspections", 161, "", "c1"),
            ("Potholes Detected (D40)", 599, "", "crit"),
            ("Cracks Detected (D00-D20)", 80, "", "fair"),
            ("Critical Hazards", 193, "", "crit"),
            ("Avg Pavement Health", 47.9, "/100", "accent"),
        ]), unsafe_allow_html=True)
    """
    cards = []
    for it in items:
        if isinstance(it, dict):
            cards.append(kpi_card(it["label"], it["value"], it.get("unit", ""), it.get("tone", "accent")))
        else:
            cards.append(kpi_card(*it))
    return '<div class="rd-kpi-grid">' + "".join(cards) + "</div>"


def condition_banner(score, rating: str, message: str, meta: str = "", max_score: int = 100) -> str:
    """The Road Condition banner. The colour follows the rating (GOOD/FAIR/POOR/CRITICAL).

        st.markdown(condition_banner(75.0, "FAIR", "Surface distress detected. ...", "Total Defects: 1 | ..."),
                    unsafe_allow_html=True)
    """
    tone = tone_for_rating(rating)
    title = f"Road Condition Score: {score:g} / {max_score} ({str(rating).upper()})"
    meta_html = f'<p class="rd-banner__meta">{html.escape(meta)}</p>' if meta else ""
    return (
        f'<div class="rd-banner rd-banner--{tone}">'
        f'<h2 class="rd-banner__title">{html.escape(title)}</h2>'
        f'<p class="rd-banner__msg">{html.escape(message)}</p>'
        f"{meta_html}</div>"
    )


# --------------------------------------------------------------------------
# matplotlib
# --------------------------------------------------------------------------
def apply_matplotlib_theme(font_dir: str | None = None) -> None:
    """Dark card-coloured charts with muted axes. Affects every figure created afterwards."""
    import matplotlib as mpl
    from cycler import cycler
    from matplotlib import font_manager as fm

    if font_dir:
        import glob
        import os

        for path in glob.glob(os.path.join(font_dir, "*.ttf")):
            fm.fontManager.addfont(path)

    families = []
    for fam in ("Inter", "DejaVu Sans"):
        try:
            fm.findfont(fam, fallback_to_default=False)
            families.append(fam)
        except Exception:
            pass
    families = families or ["sans-serif"]

    p = PALETTE
    mpl.rcParams.update({
        "figure.facecolor": p["card"], "axes.facecolor": p["card"],
        "savefig.facecolor": p["card"], "figure.edgecolor": p["card"],
        "figure.dpi": 150,
        "font.family": "sans-serif", "font.sans-serif": families,
        "text.color": p["text"],
        "axes.edgecolor": p["border"], "axes.linewidth": 0.8,
        "axes.labelcolor": p["muted"], "axes.labelsize": 10,
        "axes.titlecolor": p["text"], "axes.titlesize": 12, "axes.titleweight": "semibold",
        "axes.titlelocation": "left", "axes.titlepad": 12,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "axes.grid.axis": "y", "axes.axisbelow": True,
        "grid.color": p["grid"], "grid.linewidth": 0.8,
        "xtick.color": p["muted"], "ytick.color": p["muted"],
        "xtick.labelsize": 9, "ytick.labelsize": 9,
        "xtick.major.size": 0, "ytick.major.size": 0,
        "legend.frameon": False, "legend.fontsize": 9, "legend.labelcolor": p["muted"],
        "lines.linewidth": 1.7,
        "axes.prop_cycle": cycler(color=CATEGORICAL),
    })


def draw_pie(ax, values, labels, colors=None):
    """Damage-category pie with a clean legend instead of overlapping slice labels."""
    colors = colors or CATEGORICAL
    total = float(sum(values)) or 1.0
    wedges, _ = ax.pie(
        values, colors=colors[: len(values)], startangle=90, counterclock=False,
        wedgeprops=dict(edgecolor=PALETTE["card"], linewidth=1.5),
    )
    ax.legend(
        wedges, [f"{lab}   {v / total * 100:.1f}%" for lab, v in zip(labels, values)],
        loc="center left", bbox_to_anchor=(1.0, 0.5), labelcolor=PALETTE["text"],
    )
    ax.set_aspect("equal")
    ax.grid(False)
    return ax


def draw_bars(ax, labels, values, colors=None, value_labels=True):
    """Vertical bars (e.g. severity counts). colors: list, or None to use SEVERITY_COLORS by label."""
    if colors is None:
        colors = [SEVERITY_COLORS.get(l, PALETTE["c1"]) for l in labels]
    bars = ax.bar(labels, values, color=colors, width=0.5)
    if value_labels:
        for b, v in zip(bars, values):
            ax.annotate(f"{v:g}", (b.get_x() + b.get_width() / 2, b.get_height()),
                        ha="center", va="bottom", xytext=(0, 4), textcoords="offset points",
                        fontsize=9, color=PALETTE["muted"])
    ax.grid(axis="x", visible=False)
    return ax
