"""Build the Lebanon Graduate Futures dashboard from the clean Excel workbook.

Usage (from the repository root):
    python scripts/build_dashboard.py

Reads   data/Lebanon_Graduate_Futures_Data.xlsx
Uses    src/template.html
Writes  docs/index.html   (self-contained page served by GitHub Pages)
        docs/data.json    (every number the page uses, for checking)

Every figure quoted in the page text is computed here and inserted through a
{{placeholder}}, so the text cannot drift away from the data. The build stops
if any placeholder is left unfilled.
"""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
XLSX = ROOT / "data" / "Lebanon_Graduate_Futures_Data.xlsx"
TEMPLATE = ROOT / "src" / "template.html"
OUT_DIR = ROOT / "docs"

PEERS = ["LBN", "JOR", "EGY", "TUN", "MAR", "CYP"]  # countries in the regression
COMPARATORS = ["Jordan", "Egypt", "Tunisia", "Morocco", "Cyprus", "Arab World", "World"]

# Indicators offered in the data explorer: column -> (label, unit, modelled?)
EXPLORER = {
    "youth_unemp_total": ("Youth unemployment, ages 15-24", "% of youth labour force", True),
    "unemp_total": ("Unemployment, all ages", "% of labour force", True),
    "emp_pop_ratio": ("Employment-to-population ratio", "% of population 15+", True),
    "lfp_f": ("Labour force participation, women", "% of women 15+", True),
    "lfp_m": ("Labour force participation, men", "% of men 15+", True),
    "tertiary_enrol": ("Tertiary enrolment, gross", "% of age group", False),
    "edu_spend_gdp": ("Public education spending", "% of GDP", False),
    "remit_pct_gdp": ("Remittances received", "% of GDP", False),
    "gdp_pc_usd": ("GDP per capita", "current US$", False),
    "gdp_pc_growth": ("GDP per capita growth", "annual %", False),
    "inflation": ("Inflation, consumer prices", "annual %", False),
    "sci_articles": ("Scientific and technical articles", "articles", False),
    "net_migration": ("Net migration", "people", False),
}


def r(x, n=1):
    return None if pd.isna(x) else round(float(x), n)


def series(df, country, col, n=2):
    s = df[(df.country == country)].dropna(subset=[col]).sort_values("year")
    return {"x": s.year.astype(int).tolist(), "y": [r(v, n) for v in s[col]]}


def latest(df, country, col):
    s = df[(df.country == country)].dropna(subset=[col]).sort_values("year")
    return (int(s.year.iloc[-1]), float(s[col].iloc[-1])) if len(s) else (None, None)


def main():
    xl = XLSX
    panel = pd.read_excel(xl, "Panel_2008_2024")
    survey = pd.read_excel(xl, "Survey_Figures")
    svm = pd.read_excel(xl, "Survey_vs_Modelled").dropna(subset=["Survey period"])
    gaps = pd.read_excel(xl, "Gaps").dropna(subset=["Gap"])
    readme = pd.read_excel(xl, "README", header=None)[0].dropna().tolist()

    # ---------- survey figures with verification status ----------
    survey["verified"] = survey["Verification status"].str.startswith("Verified")
    S = {}
    for _, row in survey.iterrows():
        S[(row.Indicator, str(row.Period))] = {
            "value": float(row.Value),
            "verified": bool(row.verified),
            "status": row["Verification status"],
            "source": row.Source,
        }

    def sv(ind, per):
        return S[(ind, per)]["value"]

    lbn = panel[panel.iso3 == "LBN"].set_index("year")

    # ---------- exhibit data ----------
    D = {}
    D["modelled"] = {
        "youth": series(panel, "Lebanon", "youth_unemp_total"),
        "total": series(panel, "Lebanon", "unemp_total"),
    }
    D["survey"] = {
        "total": {"x": [2018.5, 2022.04], "y": [sv("unemployment_total", "2018-19"), sv("unemployment_total", "2022-01")],
                  "label": ["2018-19", "Jan 2022"], "verified": [S[("unemployment_total", "2018-19")]["verified"], S[("unemployment_total", "2022-01")]["verified"]]},
        "youth": {"x": [2018.5, 2022.04], "y": [sv("youth_unemployment", "2018-19"), sv("youth_unemployment", "2022-01")],
                  "label": ["2018-19", "Jan 2022"], "verified": [S[("youth_unemployment", "2018-19")]["verified"], S[("youth_unemployment", "2022-01")]["verified"]]},
    }
    D["svm"] = [
        {"indicator": row["Indicator (Lebanon)"], "period": str(row["Survey period"]),
         "survey": r(row["Survey value (%)"]), "modelled": r(row["Modelled value (%)"]),
         "gap": r(row["Gap: survey minus modelled (pp)"])}
        for _, row in svm.iterrows()
    ]

    # Index 2018 = 100 for Lebanon
    idx_cols = {"gdp_pc_usd": "GDP per capita (US$)", "tertiary_enrol": "Tertiary enrolment (gross %)",
                "remit_usd": "Remittances received (US$)", "sci_articles": "Scientific articles"}
    D["index"] = {}
    for col, lab in idx_cols.items():
        s = lbn[col].dropna()
        s = s[s.index >= 2010]
        base = s.loc[2018]
        D["index"][lab] = {"x": s.index.astype(int).tolist(), "y": [r(v / base * 100) for v in s],
                           "raw": [r(v, 1) for v in s]}

    lfs_rows = [("Unemployment", "unemployment_total"), ("Youth unemployment", "youth_unemployment"),
                ("Youth underutilisation", "youth_underutilisation"), ("Informal employment", "informal_employment"),
                ("NEET, young women", "neet_female"), ("NEET, young men", "neet_male")]
    D["lfs"] = {"labels": [a for a, _ in lfs_rows],
                "y2019": [sv(b, "2018-19") for _, b in lfs_rows],
                "y2022": [sv(b, "2022-01") for _, b in lfs_rows],
                "v2019": [S[(b, "2018-19")]["verified"] for _, b in lfs_rows],
                "v2022": [S[(b, "2022-01")]["verified"] for _, b in lfs_rows]}

    D["emig_groups"] = {"All adults": sv("want_emigrate_all", "2024"), "Aged 18-29": sv("want_emigrate_18_29", "2024"),
                        "Aged 30+": sv("want_emigrate_30plus", "2024"), "University educated": sv("want_emigrate_university", "2024"),
                        "Less educated": sv("want_emigrate_less_educated", "2024")}
    trend_years = ["2007", "2012", "2018", "2022", "2024"]
    D["emig_trend"] = {"x": [int(y) for y in trend_years], "y": [sv("want_emigrate_all", y) for y in trend_years]}

    D["remit"] = {c: series(panel, c, "remit_pct_gdp") for c in ["Lebanon"] + COMPARATORS}

    def bars(col, exclude_before=2015):
        out = {}
        for c in ["Lebanon"] + COMPARATORS:
            y, v = latest(panel, c, col)
            if y is not None and y >= exclude_before:
                out[c] = {"value": r(v), "year": y}
        return out

    D["edu"] = bars("edu_spend_gdp")
    D["tert"] = bars("tertiary_enrol")
    D["lfp"] = {"female": series(panel, "Lebanon", "lfp_f"), "male": series(panel, "Lebanon", "lfp_m"),
                "survey": {"female": sv("lfp_female", "2022-01"), "male": sv("lfp_male", "2022-01")}}

    # ---------- regression on the clean panel ----------
    reg = panel[panel.iso3.isin(PEERS)].dropna(
        subset=["youth_unemp_total", "gdp_pc_growth", "tertiary_enrol", "lfp_f", "remit_pct_gdp"])
    m = smf.ols("youth_unemp_total ~ gdp_pc_growth + tertiary_enrol + lfp_f + remit_pct_gdp + C(iso3)",
                data=reg).fit(cov_type="HC1")
    terms = [("gdp_pc_growth", "GDP per capita growth (+1 pt)"), ("tertiary_enrol", "Tertiary enrolment (+1 pt)"),
             ("lfp_f", "Female participation (+1 pt)"), ("remit_pct_gdp", "Remittances, % GDP (+1 pt)")]
    ci = m.conf_int()
    D["model"] = {"labels": [b for _, b in terms], "coef": [r(m.params[a], 3) for a, _ in terms],
                  "lo": [r(ci.loc[a, 0], 3) for a, _ in terms], "hi": [r(ci.loc[a, 1], 3) for a, _ in terms],
                  "p": [r(m.pvalues[a], 3) for a, _ in terms], "n": int(m.nobs), "r2": r(m.rsquared, 2),
                  "years": [int(reg.year.min()), int(reg.year.max())]}

    # ---------- explorer panel ----------
    D["explorer"] = {"countries": ["Lebanon"] + COMPARATORS, "indicators": {}}
    for col, (lab, unit, modelled) in EXPLORER.items():
        D["explorer"]["indicators"][col] = {
            "label": lab, "unit": unit, "modelled": modelled,
            "data": {c: series(panel, c, col, 3) for c in ["Lebanon"] + COMPARATORS}}

    D["gaps"] = [{"n": int(g["#"]), "gap": g.Gap, "why": g["Why it matters"], "have": g["What we have now"],
                  "next": g["Next step"], "priority": g.Priority} for _, g in gaps.iterrows()]

    D["simdefault"] = {"unemp": sv("youth_unemployment", "2022-01"),
                       "students": int(sv("tertiary_students", "2019-20")),
                       "want_univ": sv("want_emigrate_university", "2024")}

    # ---------- numbers quoted in the text ----------
    gdp18, gdp23 = lbn.gdp_pc_usd.loc[2018], lbn.gdp_pc_usd.loc[2023]
    remit_18_23 = lbn.remit_usd.loc[2018:2023]
    youth_gap = next(g for g in D["svm"] if g["indicator"].startswith("Youth") and g["period"] == "2022-01")
    jor_rem = panel[(panel.iso3 == "JOR") & (panel.year == 2023)].remit_pct_gdp.iloc[0]
    world_edu_y, world_edu = latest(panel, "World", "edu_spend_gdp")
    lbn_edu_y, lbn_edu = latest(panel, "Lebanon", "edu_spend_gdp")
    lbn_tert_y, lbn_tert = latest(panel, "Lebanon", "tertiary_enrol")
    n_sec = int((~survey.verified).sum())
    n_high = int((gaps.Priority == "High").sum())
    mc = dict(zip([a for a, _ in terms], range(4)))

    def badge(ind, per):
        s = S[(ind, per)]
        cls, txt = ("ok", "verified") if s["verified"] else ("sec", "secondary source")
        return f'<span class="badge {cls}" title="{s["status"]}">{txt}</span>'

    T = {
        "youth_19": f'{sv("youth_unemployment", "2018-19"):.1f}',
        "youth_22": f'{sv("youth_unemployment", "2022-01"):.1f}',
        "unemp_22": f'{sv("unemployment_total", "2022-01"):.1f}',
        "unemp_19": f'{sv("unemployment_total", "2018-19"):.1f}',
        "mod_unemp_22": f'{lbn.unemp_total.loc[2022]:.1f}',
        "mod_unemp_19": f'{lbn.unemp_total.loc[2019]:.1f}',
        "mod_youth_22": f'{lbn.youth_unemp_total.loc[2022]:.1f}',
        "youth_gap_pts": f'{youth_gap["gap"]:.1f}',
        "youth_ratio_pct": f'{lbn.youth_unemp_total.loc[2022] / sv("youth_unemployment", "2022-01") * 100:.0f}',
        "b_youth_22": badge("youth_unemployment", "2022-01"),
        "b_youth_19": badge("youth_unemployment", "2018-19"),
        "b_unemp_22": badge("unemployment_total", "2022-01"),
        "b_under_22": badge("youth_underutilisation", "2022-01"),
        "b_emig": badge("want_emigrate_university", "2024"),
        "tert_18": f'{lbn.tertiary_enrol.loc[2018]:.1f}', "tert_22": f'{lbn.tertiary_enrol.loc[2022]:.1f}',
        "gdp_fall": f'{(1 - gdp23 / gdp18) * 100:.0f}', "gdp_23": f'{gdp23:,.0f}', "gdp_24": f'{lbn.gdp_pc_usd.loc[2024]:,.0f}',
        "epr_19": f'{sv("emp_pop_ratio", "2018-19"):.1f}', "epr_22": f'{sv("emp_pop_ratio", "2022-01"):.1f}',
        "under_22": f'{sv("youth_underutilisation", "2022-01"):.1f}',
        "ltu_22": f'{sv("long_term_unemployed_share", "2022-01"):.1f}',
        "em_univ": f'{sv("want_emigrate_university", "2024"):.0f}', "em_less": f'{sv("want_emigrate_less_educated", "2024"):.0f}',
        "em_young": f'{sv("want_emigrate_18_29", "2024"):.0f}', "em_old": f'{sv("want_emigrate_30plus", "2024"):.0f}',
        "em_all": f'{sv("want_emigrate_all", "2024"):.0f}', "em_2018": f'{sv("want_emigrate_all", "2018"):.0f}',
        "rem_min": f'{remit_18_23.min() / 1e9:.1f}', "rem_max": f'{remit_18_23.max() / 1e9:.1f}',
        "gdpusd_18": f'{lbn.gdp_usd.loc[2018] / 1e9:.1f}', "gdpusd_23": f'{lbn.gdp_usd.loc[2023] / 1e9:.1f}',
        "rem_pct_18": f'{lbn.remit_pct_gdp.loc[2018]:.1f}', "rem_pct_23": f'{lbn.remit_pct_gdp.loc[2023]:.1f}',
        "jor_rem_23": f'{jor_rem:.1f}', "rem_ratio": f'{lbn.remit_pct_gdp.loc[2023] / jor_rem:.0f}',
        "rem_usd_23": f'{lbn.remit_usd.loc[2023] / 1e9:.1f}',
        "edu_lbn": f'{lbn_edu:.1f}', "edu_lbn_y": str(lbn_edu_y), "edu_world": f'{world_edu:.1f}', "edu_world_y": str(world_edu_y),
        "tert_lbn": f'{lbn_tert:.1f}', "tert_lbn_y": str(lbn_tert_y),
        "lfp_f_22": f'{sv("lfp_female", "2022-01"):.0f}', "lfp_m_22": f'{sv("lfp_male", "2022-01"):.0f}',
        "art_10": f'{lbn.sci_articles.loc[2010]:,.0f}', "art_23": f'{lbn.sci_articles.loc[2023]:,.0f}',
        "m_growth": f'{abs(m.params["gdp_pc_growth"]):.2f}', "m_growth_p": f'{m.pvalues["gdp_pc_growth"]:.3f}',
        "m_rem": f'{m.params["remit_pct_gdp"]:.2f}', "m_rem_p": f'{m.pvalues["remit_pct_gdp"]:.2f}',
        "m_lfp": f'{m.params["lfp_f"]:.2f}', "m_lfp_p": f'{m.pvalues["lfp_f"]:.3f}', "m_n": str(int(m.nobs)),
        "m_y0": str(int(reg.year.min())), "m_y1": str(int(reg.year.max())),
        "students": f'{int(sv("tertiary_students", "2019-20")):,}',
        "n_ind": str(len(EXPLORER)),
        "n_secondary": str(n_sec), "n_survey": str(len(survey)), "n_gaps": str(len(gaps)), "n_high": str(n_high),
        "build_date": dt.date.today().strftime("%d %B %Y"),
        "workbook_date": next((re.search(r"Prepared (\d+ \w+ \d{4})", s).group(1) for s in readme if "Prepared" in str(s)), "[to confirm]"),
    }

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("__DATA__", json.dumps(D, ensure_ascii=False, separators=(",", ":")))
    html = re.sub(r"\{\{(\w+)\}\}", lambda mt: T[mt.group(1)], html)
    left = re.findall(r"\{\{\w+\}\}", html)
    if left:
        raise SystemExit(f"Unfilled placeholders: {left}")

    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "index.html").write_text(html, encoding="utf-8")
    (OUT_DIR / "data.json").write_text(json.dumps({"text_values": T, "chart_data": D}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Built docs/index.html ({len(html) / 1024:.0f} KB) from {XLSX.name}")
    print(f"Regression: n={int(m.nobs)}, R2={m.rsquared:.2f}, growth {m.params['gdp_pc_growth']:+.3f} (p={m.pvalues['gdp_pc_growth']:.3f}), "
          f"remittances {m.params['remit_pct_gdp']:+.3f} (p={m.pvalues['remit_pct_gdp']:.3f})")
    print(f"Survey rows still on secondary sources: {n_sec} of {len(survey)}")


if __name__ == "__main__":
    main()
