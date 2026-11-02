# Changes from the October proposal dashboard

## Data (now built from the clean workbook of 20 October 2026)
- 2018-19 youth unemployment corrected from 23.0% (UNDP blog) to **23.3%** (CAS report, Table 3.8).
- Exhibit 1 now uses the total youth unemployment series (`youth_unemp_total`) instead of separate female and male lines, and adds a third view drawn from the `Survey_vs_Modelled` tab.
- Panel period is 2008-2024 (previously 2005-2023 for remittances, 2000-2023 for participation).
- GDP per capita text now records the 2024 partial recovery (US$4,473).
- Public education spending chart drops Egypt (latest value 2008) and shows the year for each economy.
- **Regression refitted on the clean panel** (2008-2024, n = 98, R² = 0.68). GDP per capita growth keeps its link (−0.35 points, p = 0.002). The remittance coefficient (+0.21) is no longer significant at 5% (p = 0.10), so the heading "dependence on remittances does not [lower it]" was replaced.
- **Removed:** the "Where to" destinations chart (Canada 32%, Germany 28%, France 25%, and so on) and the claim that 72% of would-be migrants cite economic reasons. Neither figure is in the clean workbook. To restore them, add the rows to `Survey_Figures` with a verification status, then add the chart back.
- Hand-typed numbers in the text replaced by values computed at build time.

## New features
- Verification badges on every survey figure (verified or secondary source), driven by the workbook's `Verification status` column.
- Data explorer: 13 indicators, Lebanon against any of seven comparators.
- Data gaps register from the `Gaps` tab, filterable by priority.
- "Data behind this chart" table and CSV download under every chart.
- Chart titles state the finding and update with the data and the selected view.
- Light and dark theme toggle, sticky section navigation, scenario reset button, print styles, social-sharing metadata.

## Design
- Blue and orange palette replacing gold, oxblood, teal and navy.
- Direct line labels instead of legends; 2018-19 vs 2022 survey comparison redrawn as a dumbbell chart instead of grouped bars.
- Significance shown by filled vs hollow markers, verification by filled vs open diamonds: colour is never the only cue.
