# Lebanon Graduate Futures

An interactive evidence dashboard on what happens to Lebanese university graduates after 2019: unemployment, emigration intentions and the diaspora economy.

MSBA 325 Data Visualization and Communication, American University of Beirut, Fall 2026. Team 5: Amal Alrajab, Hassan Halabi, Hidaya Hussein, Maya Raad and Saleh Mansour.

**Live page:** `https://github.com/SMM303/lebanon-graduate-futures/` (active once GitHub Pages is switched on; see [PUBLISHING.md](PUBLISHING.md)).

## What the dashboard shows

| Section | Finding | Main source |
|---|---|---|
| Evidence 1 | The ILO modelled series puts 2022 youth unemployment at about half the national survey figure | World Bank WDI; CAS/ILO LFS 2018-19 and Jan 2022 |
| Evidence 2 | Tertiary enrolment rose while GDP per capita fell by almost two thirds | World Bank WDI; CAS/ILO LFS |
| Evidence 3 | Young and university-educated Lebanese are the most likely to want to emigrate | Arab Barometer 2024 |
| Evidence 4 | Remittances rose to a third of GDP | World Bank WDI |
| Evidence 5 | High enrolment, low public education spending, low female participation | World Bank WDI; CAS/ILO LFS |
| Analytics | Fixed-effects regression of youth unemployment across six countries | World Bank WDI panel |
| Scenario console | What-if model of five graduate cohorts | Stated assumptions |
| Data explorer | Lebanon against seven comparators on 13 indicators | World Bank WDI panel |
| Data gaps | The 13 gaps in the evidence, with next steps | Gaps tab of the workbook |

Every survey figure carries a badge: **verified** (checked in the primary report) or **secondary source** (not yet checked). Every chart has a finding-style title, units, year range and source line, and a "Data behind this chart" table with CSV download.

## Repository layout

```
data/Lebanon_Graduate_Futures_Data.xlsx   clean workbook (the single source of every number)
scripts/build_dashboard.py                reads the workbook, computes every figure, writes the page
src/template.html                         page design, text and chart code, with {{placeholders}}
docs/index.html                           built page served by GitHub Pages (do not edit by hand)
docs/data.json                            every number the page uses, for checking
.github/workflows/rebuild.yml             optional: rebuilds docs/ when the workbook changes
```

## Updating the data

1. Replace `data/Lebanon_Graduate_Futures_Data.xlsx` with the new version. Keep the tab names and column headers unchanged (`Panel_2008_2024`, `Survey_Figures`, `Survey_vs_Modelled`, `Data_Dictionary`, `Gaps`).
2. Rebuild:
   ```bash
   pip install -r requirements.txt
   python scripts/build_dashboard.py
   ```
3. Open `docs/index.html` in a browser and check it.
4. Commit and push. GitHub Pages republishes within a minute or two.

When a January 2022 survey value is confirmed against the CAS tables, change its `Verification status` in `Survey_Figures` so it starts with "Verified". The badge on the page switches to **verified** at the next build.

Text figures update automatically. Wording that interprets a figure (for example "doubled") is in `src/template.html` and should be reread after any large data change.

## Design choices

- Blue and orange only, plus greys. Orange marks Lebanon or the problem; blue marks benchmarks and improvement; grey keeps context in the background. Blue and orange stay distinct under red-green colour blindness, and colour is never the only cue (diamond vs circle, open vs filled, dashed vs solid, direct labels).
- Direct labels at line ends replace legends (Gestalt proximity and similarity). Light gridlines only on the value axis; no chart borders or data markers unless they carry meaning.
- One marker for the October 2019 crisis on every time series.
- Survey and modelled estimates are never merged into one line.
- Light and dark themes, keyboard focus states, text alternatives for every chart.

## Licence

Code: MIT (see `LICENSE`). Data: World Bank WDI under CC BY 4.0; survey figures belong to CAS/ILO and Arab Barometer and are cited on the page.
