# Asphalt Ochre (dark) - Implementation Spec

Audience: an AI coding agent (or a developer) applying this theme to the Streamlit app
"Smart Road Damage Detection & Inspection System" (IPCV capstone: YOLO11n, RDD2022, geo-tagged reports).

Pages covered: **app (Home)**, **Single Image Studio**, **Batch Survey Processor**, **Interactive Damage Map**,
**Inspection Reports**, **Live Training Telemetry**.

## 0. Rules for the implementer (read first)

1. **Change only the look.** Do not move, remove, rename or re-order any widget, chart, table, tab, page or sidebar item. Do not change detection logic, data, model code, file handling or database code.
2. **Use the exact values in this file** and the prepared `theme.py` / `.streamlit/config.toml`. Do not substitute colours or fonts. If something seems wrong, keep it and report it.
3. **Fonts are fixed:** `Inter` for text, `Newsreader` (serif) for headings. Never fall back to Streamlit's default font on purpose.
4. **The dark theme is final.** No white backgrounds anywhere, including matplotlib figures, tables, the file uploader and expanders.
5. **Every page file** (the main file and each file in `pages/`) must call `apply_theme()` right after `st.set_page_config(...)`. Streamlit re-runs each page separately, so CSS injected on one page does not carry over to the next.
6. Streamlit's internal CSS names change between versions. If a selector in section 7 does not match, inspect the element in the browser and correct the selector. Do not drop the rule.

## 1. Design intent

Calm, technical, road-inspection feel: warm charcoal "asphalt" surfaces, thin hairline borders, one muted ochre accent (like road markings), serif headings for an editorial touch, and semantic colours (green, amber, orange, red) used only to show road condition and severity.

## 2. Design tokens

### 2.1 Colours

| Token | Hex | Role | Contrast |
|---|---|---|---|
| `bg` | `#121315` | page background | - |
| `side` | `#0E0F11` | sidebar background | - |
| `card` | `#191A1D` | cards, inputs, tables, uploader, expanders, chart background | - |
| `border` | `#26282D` | all hairlines and card borders | decorative |
| `navactive` | `#23262B` | active or hovered sidebar page | - |
| `text` | `#ECEDEF` | headings, values, body text | 15.9:1 on bg, 14.9:1 on card |
| `muted` | `#9EA2AB` | labels, captions, axes, inactive tabs | 7.3:1 on bg, 6.8:1 on card, 5.9:1 on navactive |
| `accent` | `#D2A24C` | active tab underline, primary button, slider, radio/checkbox, progress bar, info icons | 7.5:1 on card |
| `accent_ink` | `#1B1405` | text on the ochre primary button | 7.8:1 on accent |
| `grid` | `#212328` | chart gridlines, progress track | decorative |

Semantic colours (solid / tinted background / text on the tint):

| Tone | Solid | Tint (background) | Text on tint | Meaning |
|---|---|---|---|---|
| `good` | `#6FBF8E` | `rgba(111,191,142,0.14)` | `#8FD3AA` (7.8:1) | GOOD rating, Minor severity, success |
| `fair` | `#E0B04F` | `rgba(224,176,79,0.14)` | `#EBC677` (8.1:1) | FAIR rating, Moderate severity, warning |
| `poor` | `#E8905A` | `rgba(232,144,90,0.14)` | `#F2AE82` (7.3:1) | POOR rating |
| `crit` | `#E5736A` | `rgba(229,115,106,0.14)` | `#F09A92` (6.7:1) | CRITICAL rating, Critical severity, error |

Damage-category colours (pie and category charts): Pothole D40 `#6FA0D6`, Alligator D20 `#E5736A`, Transverse D10 `#E0B04F`, Longitudinal D00 `#5CB8A8`. All are at least 5.8:1 on `card`.

Never use pure white `#FFFFFF`, pure black `#000000`, Streamlit's default red `#FF4B4B`, or saturated full-colour blocks (the old solid orange and green banners are replaced by tinted banners).

### 2.2 Typography

Loaded by `theme.py`: `Inter` 400/500/600 and `Newsreader` 500/600 from Google Fonts.

| Element | Family | Size | Weight |
|---|---|---|---|
| Page title (`st.title`) | Newsreader | 32 px (2rem) | 500, letter-spacing -0.015em |
| Section heading (`st.header`) | Newsreader | 22 px (1.375rem) | 500 |
| Sub-heading (`st.subheader`) | Newsreader | 18 px (1.125rem) | 500 |
| Sidebar headings ("Inference Controls", "IPCV Image Processing", "Navigation") | Newsreader | about 17 px | 500 |
| Body text, labels | Inter | 14 px | 400 |
| Captions, helper text | Inter | 12-13 px | 400, `muted` |
| KPI label | Inter | 11 px, uppercase, letter-spacing 0.08em | 500, `muted` |
| KPI and `st.metric` value | Inter, tabular numbers | 28 px (1.75rem) | 500 |
| Tab labels | Inter | 14 px | 500 inactive, 600 active |
| Banner title | Newsreader | 30 px | 500, coloured by tone |
| Chart text | Inter (DejaVu Sans fallback) | 9-12 px | 400, `muted` |

### 2.3 Shape and elevation

- Radius **8 px** on cards, inputs, buttons, banners, images, tables. Progress bar fully rounded.
- Borders `1px solid #26282D`. Shadow is effectively none: `0 1px 0 rgba(255,255,255,0.02)`.
- KPI card padding 16 px 18 px; banner padding 28 px 24 px; grid gap 16 px.

## 3. Page-by-page spec

Every page: dark background, Newsreader title, one `muted` description line, thin `border` dividers between sections.

**Home (app)**
- Title and description, divider.
- **Five KPI cards** in a row (`kpi_grid`): Total Inspections (dot `c1` blue), Potholes Detected D40 (dot `crit`), Cracks Detected D00-D20 (dot `fair`), Critical Hazards (dot `crit`), Avg Pavement Health with "/100" unit (dot `accent`). The old coloured left borders are replaced by a small coloured dot before the label.
- Section heading "Inspection Analytics & Damage Distribution", then tabs "Distress Analytics" and "Recent Inspection Logs".
- Two columns: pie "Damage Breakdown by Category" (`draw_pie`, legend on the right with percentages, no overlapping slice labels) and bars "Severity Rating Breakdown" (`draw_bars`: Minor green, Critical red, Moderate amber, value above each bar).
- Sidebar: page navigation, divider, "Navigation" heading, then the project info (Model YOLO11n, Target RDD2022 India, Hardware RTX 3050 Ti) as a card (`st.info` is styled as a card with an ochre icon).

**Single Image Studio**
- Radio "Choose Input Method", select box for the sample image, divider.
- **Condition banner** via `condition_banner(score, rating, message, meta)`: tinted background, thin tone-coloured border, serif title in the tone's text colour, message in `text`, meta line in `muted`. Tone follows the rating (GOOD green, FAIR amber, POOR orange, CRITICAL red).
- Two columns "Original Survey Image" and "AI Detected Road Distress" with `st.image` (8 px radius and thin border added automatically).
- Sidebar: "Inference Controls" (engine select, confidence slider, IoU slider, resolution select), divider, "IPCV Image Processing" with two checkboxes.

**Batch Survey Processor**
- Uploader (dashed border card), `st.info` "Loaded N images" (card with ochre icon), **primary button** "Process All Images" (ochre fill, dark text), progress bar (ochre fill on `grid` track), `st.success` (green tint).
- "Survey Run Summary": four `st.metric` cards without chips.
- "Inspection Reports Table": `st.dataframe`, optionally with `rating_cell_style` on the Rating column; "Download Full Batch Survey Report (CSV)" is a secondary button (card background, hover turns ochre).
- "Detailed Image Inspection Reports": each photo in an expander (card, thin border); inside, tabs "AI Detected Distress" / "Original Photo", the image, and a **condition banner** (green for GOOD) beside it, then the recommendation text and a `muted` location caption.
- Sidebar: "Batch Inference Controls" with select box and slider.

**Interactive Damage Map** (no screenshot available)
- Map container: 8 px radius, 1 px `border`. Map tiles: use a dark basemap if the library allows it (for example folium `tiles="CartoDB dark_matter"`).
- Markers by severity: Minor `good`, Moderate `fair`, Poor `poor`, Critical `crit`. Popups use `card` background and `text`.
- Everything else (headings, filters, metrics) follows the shared rules.

**Inspection Reports**
- Select box filter, subheader "Inspection Audit Records (N Entries)", `st.dataframe` (dark grid from `config.toml`), secondary download button "Export Filtered Logs as CSV".
- Rating column: apply `rating_cell_style` so Good, Fair, Poor and Critical show in their tone colours.

**Live Training Telemetry**
- Title, description. Toggle "Auto-Refresh" (ochre when on) and secondary button "Refresh Now".
- Subheader with epoch progress, progress bar, four metric cards (Elapsed Time, ETA, Estimated Completion, Average Speed).
- "Real-Time GPU Hardware Telemetry": four metric cards; chips (deltas) appear as green tinted pills (`good`).
- Tabs: Loss Curves, Accuracy & mAP Metrics, Raw Epoch Logs, Training Batches.
- Loss curves: three matplotlib panels. Train line `LOSS_TRAIN` (blue `#6FA0D6`, solid, 1.7 px), validation line `LOSS_VAL` (amber `#E0B04F`, dashed, 1.7 px). For mAP and accuracy curves use `good` and `accent`.

## 4. Component specs

- **KPI cards** (custom HTML): `card` background, border, 8 px radius; dot + uppercase label on top; 28 px value; optional muted unit.
- **`st.metric`**: same card look. Label uppercase 11 px `muted`; value 28 px; delta chip: `good` tint with `good_fg` text, 4 px radius. `delta_color="off"` is not needed because the CSS forces the chip colours.
- **Tabs**: transparent; active text `text` weight 600 with a **2 px ochre underline**; inactive `muted`; a 1 px `border` line under the row.
- **Buttons**: secondary = `card` background, 1 px border, `text`, hover border and text turn ochre. Primary = ochre fill, `accent_ink` text, weight 600.
- **Inputs** (select, uploader, text): `card` background, 1 px border, 8 px radius. Sliders, radios, checkboxes and toggles use the ochre accent.
- **Alerts**: `st.info` card with ochre icon; `st.success` green tint; `st.warning` amber tint; `st.error` red tint.
- **Expander**: card background, border, 8 px radius.
- **Images**: 8 px radius and a 1 px border.
- **Condition banner**: tinted tone background, 1 px border mixed 45 percent tone with card, centred text.

## 5. Chart spec (matplotlib)

`apply_theme()` calls `apply_matplotlib_theme()`, which sets the defaults for all figures created afterwards:
figure and axes background `card`; top and right spines off; remaining spines `border`; horizontal gridlines `grid`; tick labels `muted` 9 px with no tick marks; axis labels `muted` 10 px; titles left-aligned 12 px semibold `text`; legend with no frame; default colour cycle = the four damage-category colours; default line width 1.7.

| Chart | How |
|---|---|
| Damage category pie | `draw_pie(ax, values, labels)`: slices separated by a 1.5 px `card` edge, starting at 12 o'clock, legend to the right with percentages. Do not draw labels on the slices. |
| Severity bars | `draw_bars(ax, labels, values)`: colours from `SEVERITY_COLORS`, bar width 0.5, value label above each bar in `muted`. |
| Loss curves | `ax.plot(x, y, label="Train", **LOSS_TRAIN)` and `ax.plot(x, y, label="Val", **LOSS_VAL)`; titles in each panel; call `fig.tight_layout()`. |
| Any new chart | rely on the rcParams; if you set colours manually, take them from `PALETTE` only. |

Remove old hard-coded styling in the app: `plt.style.use(...)`, `fig.patch.set_facecolor("white")`, `sns.set_style("whitegrid")`, large default font sizes, seaborn palettes with bright greens or reds.

Optional: put Inter `.ttf` files in a folder and call `apply_theme(font_dir="path/to/fonts")` so charts also use Inter; otherwise they fall back to DejaVu Sans.

## 6. Implementation steps for the agent

1. Copy `theme.py` into the project root (next to the main Streamlit file). Copy `.streamlit/config.toml` to `<project>/.streamlit/config.toml` (merge if one exists).
2. In the main file and in **every** file under `pages/`, right after `st.set_page_config(...)` add:
   `from theme import apply_theme` then `apply_theme()`.
3. Home: replace the custom KPI HTML with `st.markdown(kpi_grid([...]), unsafe_allow_html=True)` using the same numbers. Keep the existing values.
4. Single Image Studio and Batch pages: replace the solid orange and green HTML banners with `st.markdown(condition_banner(score, rating, message, meta), unsafe_allow_html=True)`.
5. Charts: for the pie and bar charts use `draw_pie` and `draw_bars`. For other matplotlib figures just remove old styling code. Use `LOSS_TRAIN` and `LOSS_VAL` for the training curves.
6. Tables: add `df.style.map(rating_cell_style, subset=["rating"])` where a rating column is shown (use `.applymap` on older pandas).
7. Search the code (`grep -rn "style=\"\|<style\|set_facecolor\|plt.style\|#" pages app.py`) for old inline colours, custom CSS blocks and white backgrounds, and remove those that conflict.
8. Restart Streamlit fully, hard-refresh the browser (Ctrl+Shift+R), and walk through all six pages.

### Acceptance checklist (all must be true)

- [ ] Every page has the charcoal background `#121315`; no white rectangles anywhere (charts, tables, uploader, expanders, images' surrounding).
- [ ] Headings are serif (Newsreader); body text is Inter. Verify in dev tools, Computed, font-family.
- [ ] Sidebar is darker (`#0E0F11`); the current page in the page list has a highlighted pill background and bold text.
- [ ] KPI cards: card background, thin border, small coloured dot, uppercase muted label, 28 px value.
- [ ] Active tab has an ochre underline; the primary button is ochre with dark text; progress bar is ochre.
- [ ] Banners are tinted (not solid orange or green) and follow the rating colour.
- [ ] Pie and bar charts have no white background, readable muted axes, legend instead of overlapping labels, severity colours green, red, amber.
- [ ] Loss curves: blue solid train line, amber dashed validation line, dark card background.
- [ ] Tables are dark with thin borders; ratings are coloured by tone.
- [ ] Layout, widgets, order, data and behaviour are identical to before theming.

## 7. Streamlit selector map (inside `_CSS` in `theme.py`)

| UI part | Selector |
|---|---|
| Page, header | `.stApp`, `[data-testid="stAppViewContainer"]`, `[data-testid="stHeader"]` |
| Sidebar | `[data-testid="stSidebar"]` |
| Page navigation links | `[data-testid="stSidebarNav"] a`, `[data-testid="stSidebarNavLink"]`, active: `[aria-current="page"]` |
| Tabs | `button[data-baseweb="tab"]`, `[data-baseweb="tab-highlight"]`, `[data-baseweb="tab-border"]` |
| Metrics | `[data-testid="stMetric"]`, `stMetricLabel`, `stMetricValue`, `stMetricDelta` |
| Buttons | `.stButton > button`, `button[kind="primary"]`, `[data-testid="stBaseButton-primary"]`, `[data-testid="stDownloadButton"] > button` |
| Select | `[data-baseweb="select"] > div` |
| Slider handle | `[data-testid="stSlider"] [role="slider"]` |
| Uploader | `[data-testid="stFileUploaderDropzone"]`, `[data-testid="stFileUploaderFile"]` |
| Progress | `[data-testid="stProgress"] [role="progressbar"]` and its first child |
| Alerts | `[data-testid="stAlert"]` with `:has([data-testid="stAlertContentSuccess"])` and the Info, Warning, Error variants |
| Expander | `[data-testid="stExpander"] details` |
| Images | `[data-testid="stImage"] img`, `[data-testid="stImageContainer"] img` |
| Table | `[data-testid="stDataFrame"]` |
| Custom classes from helpers | `.rd-kpi-grid`, `.rd-kpi`, `.rd-banner`, `.rd-banner--good|fair|poor|crit` |

## 8. Common failure points

| Symptom | Cause | Fix |
|---|---|---|
| Other pages still look default | `apply_theme()` only called in the main file | call it in every file in `pages/` |
| Page is not dark | `config.toml` missing or server not restarted | place it in `<project>/.streamlit/`, restart |
| Default font | CSS not injected, or no internet for Google Fonts | check call order; check network |
| KPI cards or banners show raw HTML | `unsafe_allow_html=True` missing | add it to `st.markdown` |
| Charts have white background | old `plt.style.use`, `set_facecolor` or `sns.set_style` code overrides the theme, or `apply_theme()` runs after the figure is created | remove it; call `apply_theme()` at the top |
| Pie labels overlap | slice labels still drawn | use `draw_pie` (legend) |
| Sidebar nav not highlighted | different Streamlit version | inspect the link, adjust the `stSidebarNav` selector |
| Progress bar not ochre | internal structure differs | inspect `[role="progressbar"]` and adjust the selector |
| Table too bright or white | table colours come from `config.toml` | check `base = "dark"` and colour keys |

## 9. Do and don't

- Do keep the ochre accent for interaction (active tab, primary action, sliders, progress). Use green, amber, orange and red only for condition and severity.
- Do keep thin borders, generous spacing and calm contrast.
- Don't add gradients, glows, neon colours, emojis in headings, or solid saturated colour blocks.
- Don't change fonts, add colours outside the tokens, or touch detection logic and data.

## 10. Ready-to-paste prompt for your AI agent

> Apply the "Asphalt Ochre (dark)" theme to this Streamlit app by following THEME_SPEC.md exactly. Use the provided `theme.py` and `.streamlit/config.toml` as they are. Do not change layout, widgets, data, detection logic or fonts (Inter for text, Newsreader for headings). Steps: copy the files; call `apply_theme()` right after `st.set_page_config` in the main file and in every file under `pages/`; replace the KPI cards with `kpi_grid(...)` and the solid orange/green result banners with `condition_banner(...)` (both rendered with `st.markdown(..., unsafe_allow_html=True)`); style the pie and bar charts with `draw_pie` and `draw_bars` and the training curves with `LOSS_TRAIN`/`LOSS_VAL`; colour rating columns with `rating_cell_style`; remove conflicting old CSS, matplotlib styles and white backgrounds; restart Streamlit; then verify every item in the acceptance checklist on all six pages. Report anything you could not match, with the page, the element and the reason.
