# lebanon-graduate-futures
Interactive dashboard on Lebanese university graduates since 2019: unemployment, emigration intentions and remittances, with a scenario console. MSBA 325, Team 5, American University of Beirut.
# Lebanon Graduate Futures

**Live dashboard:** https://smm303.github.io/lebanon-graduate-futures/

An interactive dashboard on what has happened to Lebanese university graduates since the 2019 financial collapse: unemployment, emigration intentions, remittances and public investment in education, with a scenario console that tests how policy measures could change graduate outcomes.

MSBA 325, Data Visualization and Communication, Suliman S. Olayan School of Business, American University of Beirut, Fall 2026. Instructor: Dr Zablit.

## Key findings

- Youth unemployment rose from 23.0% (2018–19) to 47.8% (January 2022), according to the CAS/ILO Labour Force Surveys.
- ILO modelled estimates show Lebanon's total unemployment at 11.1% in 2022, against 29.6% in the national survey. Global datasets understate the crisis.
- 46% of university-educated Lebanese wanted to emigrate in 2024, against 33% of the less educated (Arab Barometer Wave VIII).
- Remittances rose from 12.7% of GDP (2018) to 33.3% (2023), about four times Jordan's share (World Bank WDI).
- Public spending on education stands at 1.2% of GDP (2024), against a world average of 3.6% (World Bank WDI).

## What the dashboard contains

| Section | Content | Interaction |
|---|---|---|
| Evidence 1 | Modelled versus surveyed unemployment | All ages / youth toggle |
| Evidence 2 | Enrolment, GDP per capita, remittances and research output, indexed to 2018; survey indicators 2019 vs 2022 | Two views |
| Evidence 3 | Emigration intentions by group, trend since 2007, preferred destinations | Three views |
| Evidence 4 | Remittances as a share of GDP, Lebanon against peers | Legend filter by country |
| Evidence 5 | Education spending, tertiary enrolment, labour force participation by sex | Three views |
| Analytics | Fixed-effects regression on drivers of youth unemployment | Hover for estimates and p-values |
| Scenario console | Five-cohort what-if model of graduate employment and emigration | Six sliders |
| Strategic reading | Gaps, strengths and opportunities | |

The page adapts to mobile screens and follows the device's light or dark setting.

## Data sources

1. World Bank, World Development Indicators, including ILO modelled estimates, via the open [datasets/world-development-indicators](https://github.com/datasets/world-development-indicators) mirror (CC BY 4.0), accessed October 2026.
2. Central Administration of Statistics and ILO, Lebanon Labour Force and Household Living Conditions Survey 2018–19 and Follow-up Labour Force Survey, January 2022.
3. Arab Barometer, [Lebanon Migration Insights 2024](https://www.arabbarometer.org/2024/08/lebanon-migration-insights-2024-public-opinion-factsheet/), and earlier waves.
4. CRDP statistical bulletin 2019–20, via Information International.

Comparators: Jordan, Egypt, Tunisia, Morocco, Cyprus, the Arab World aggregate and the World.

## Limitations

- ILO series for Lebanon are modelled estimates, not survey results, and are labelled as such throughout.
- The most recent national labour force survey in our sources dates from January 2022.
- No official statistic counts emigrant graduates; emigration is shown through stated intentions.
- No graduate tracer data exists by university or field of study.
- The regression shows associations in modelled data, not causal effects.
- The scenario console is a transparent what-if tool built on stated assumptions, not a forecast.

## Files

| File | Purpose |
|---|---|
| `index.html` | The dashboard: a single self-contained page using Plotly.js |
| `build_dataset.py` | Python script that assembles the WDI panel and national figures |
| `lebanon_graduates_wdi_panel.csv` | WDI panel, 2005–2024, Lebanon and comparators |
| `lebanon_graduates_national_figures.csv` | National survey and opinion figures, with source links |

## Team 5

Amal Al Rajab, Hassan Halabi, Hidaya Hussein, Maya Raad, Saleh Mansour (coordinator).
