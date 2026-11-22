# Asphalt Ochre (dark) theme for the Road Damage Inspection app

Fonts: **Inter** (text) and **Newsreader** (headings), loaded from Google Fonts.
Palette: warm charcoal surfaces, thin borders, one muted ochre accent, green / amber / orange / red for road condition.

## What is in this folder

```
asphalt_ochre_theme/
├── .streamlit/config.toml   native dark theme colours
├── theme.py                 CSS, KPI + banner helpers, matplotlib chart style
├── example_app.py           runnable preview with sample data
├── THEME_SPEC.md            full written spec for your AI agent (all six pages, checklist, prompt)
└── README.md
```

## Apply it in 5 steps

1. Copy `theme.py` next to your main Streamlit file. Copy `config.toml` into a `.streamlit/` folder in the same place (merge the `[theme]` block if you already have one).
2. In the main file **and in every file inside `pages/`**, directly after `st.set_page_config(...)`:

   ```python
   from theme import apply_theme
   apply_theme()
   ```
3. Home page KPI cards:

   ```python
   from theme import kpi_grid
   st.markdown(kpi_grid([
       ("Total Inspections", 161, "", "c1"),
       ("Potholes Detected (D40)", 599, "", "crit"),
       ("Cracks Detected (D00-D20)", 80, "", "fair"),
       ("Critical Hazards", 193, "", "crit"),
       ("Avg Pavement Health", 47.9, "/100", "accent"),
   ]), unsafe_allow_html=True)
   ```
4. Result banners (Single Image Studio and Batch reports). The colour follows the rating:

   ```python
   from theme import condition_banner
   st.markdown(condition_banner(75.0, "FAIR", "Surface distress detected. Preventative crack sealing recommended.",
                                "Total Defects: 1 | Engine: Ensemble Fusion (Recommended)"),
               unsafe_allow_html=True)
   ```
5. Restart Streamlit completely (stop it, then `streamlit run app.py`), and hard-refresh the browser with Ctrl+Shift+R.

To preview the theme first: `pip install streamlit matplotlib pandas numpy`, then `streamlit run example_app.py`.

## Charts (matplotlib)

`apply_theme()` already makes every matplotlib figure dark and clean. For your two Home charts and the training curves:

```python
from theme import draw_pie, draw_bars, LOSS_TRAIN, LOSS_VAL

fig, ax = plt.subplots(figsize=(6.4, 4.2))
draw_pie(ax, values, labels)              # legend instead of overlapping labels
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(6.4, 4.2))
draw_bars(ax, ["Minor", "Critical", "Moderate"], counts)   # green / red / amber
st.pyplot(fig)

ax.plot(epochs, train_loss, label="Train", **LOSS_TRAIN)   # blue, solid
ax.plot(epochs, val_loss, label="Val", **LOSS_VAL)         # amber, dashed
```

Remove any old `plt.style.use(...)`, `fig.patch.set_facecolor("white")` or `sns.set_style(...)` lines; they override the theme.

## Tables

```python
from theme import rating_cell_style
st.dataframe(df.style.map(rating_cell_style, subset=["rating"]), use_container_width=True)
```
(Use `.applymap` instead of `.map` on older pandas.)

## Optional

- `apply_theme(hide_chrome=True)` hides the Deploy button, menu and footer (nice for demos).
- `apply_theme(font_dir="fonts")` lets matplotlib charts use Inter if you put the Inter `.ttf` files in that folder.
- To change the accent, edit `PALETTE["accent"]` in `theme.py` and `primaryColor` in `config.toml`.

## Troubleshooting

- **Only the home page is themed.** Call `apply_theme()` in every file in `pages/`.
- **Banners or cards show raw HTML text.** Add `unsafe_allow_html=True` to that `st.markdown`.
- **Charts still white or default.** Remove old styling code; make sure `apply_theme()` runs before the figure is created.
- **Fonts look default.** The browser could not reach Google Fonts; check your internet connection.
- **A part is not styled.** Streamlit's internal element names change between versions: right-click the element, Inspect, and update the matching selector in `_CSS` in `theme.py` (the table in `THEME_SPEC.md` section 7 lists them all).
- **Warning about `use_container_width`.** Newer Streamlit prefers `width="stretch"`; both work for now.
