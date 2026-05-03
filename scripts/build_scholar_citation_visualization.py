#!/usr/bin/env python3
"""Build the static ACM Fellow citation timeline visualization."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


APP_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ACM = APP_ROOT / "data" / "acm_fellows.csv"
DEFAULT_SCHOLAR = APP_ROOT / "data" / "google_scholar_profiles.csv"
DEFAULT_OUTPUT = APP_ROOT / "docs" / "scholar_citations.html"

HTML_TEMPLATE = '<!doctype html>\n<html lang="en">\n<head>\n  <meta charset="utf-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <title>ACM Fellow Citation Timelines</title>\n  <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>\n  <style>\n    :root {\n      color-scheme: light;\n      --bg: #f7f7f4;\n      --panel: #ffffff;\n      --ink: #202124;\n      --muted: #686f78;\n      --line: #d9ddd5;\n      --soft-line: #eceee8;\n      --accent: #246b5c;\n      --accent-soft: #dcebe6;\n      --bar: #3e7c6b;\n      --bar-muted: #cbd4ce;\n      --missing: #a4aaa3;\n      --row-h: 32px;\n      --chart-h: 22px;\n      --year-w: 13px;\n      --label-w: 280px;\n      --citations-w: 92px;\n      --h-index-w: 58px;\n      --chart-pad-r: 28px;\n    }\n    * { box-sizing: border-box; }\n    body {\n      margin: 0;\n      background: var(--bg);\n      color: var(--ink);\n      font: 13px/1.35 ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;\n    }\n    header {\n      position: sticky;\n      top: 0;\n      z-index: 10;\n      background: rgba(247, 247, 244, 0.96);\n      border-bottom: 1px solid var(--line);\n      backdrop-filter: blur(8px);\n    }\n    .topbar {\n      max-width: 1280px;\n      margin: 0 auto;\n      padding: 14px 20px 12px;\n    }\n    h1 {\n      margin: 0 0 10px;\n      font-size: 20px;\n      font-weight: 700;\n      letter-spacing: 0;\n    }\n    .controls {\n      display: grid;\n      grid-template-columns: minmax(220px, 360px) repeat(2, max-content) 1fr;\n      gap: 12px;\n      align-items: center;\n    }\n    input[type="search"] {\n      width: 100%;\n      height: 34px;\n      border: 1px solid var(--line);\n      border-radius: 6px;\n      padding: 0 10px;\n      background: white;\n      color: var(--ink);\n      font: inherit;\n    }\n    label.toggle {\n      display: inline-flex;\n      align-items: center;\n      gap: 6px;\n      color: var(--muted);\n      white-space: nowrap;\n      user-select: none;\n    }\n    .summary {\n      justify-self: end;\n      color: var(--muted);\n      white-space: nowrap;\n      font-variant-numeric: tabular-nums;\n    }\n    main {\n      max-width: 1280px;\n      margin: 0 auto;\n      padding: 12px 20px 28px;\n    }\n    .table {\n      min-width: calc(var(--label-w) + var(--citations-w) + var(--h-index-w) + ((2026 - 1986 + 1) * var(--year-w)) + var(--chart-pad-r) + 120px);\n      background: var(--panel);\n      border: 1px solid var(--line);\n      border-radius: 8px;\n      overflow: hidden;\n      box-shadow: 0 1px 2px rgba(0,0,0,0.03);\n    }\n    .row {\n      display: grid;\n      grid-template-columns: 58px var(--label-w) var(--citations-w) var(--h-index-w) 1fr;\n      align-items: center;\n      min-height: var(--row-h);\n      border-bottom: 1px solid var(--soft-line);\n      padding: 0 10px;\n      column-gap: 10px;\n    }\n    .row:last-child { border-bottom: 0; }\n    .head {\n      min-height: 34px;\n      background: #eef1eb;\n      color: var(--muted);\n      font-size: 11px;\n      font-weight: 700;\n      text-transform: uppercase;\n      letter-spacing: .04em;\n      border-bottom: 1px solid var(--line);\n    }\n    .year {\n      color: var(--muted);\n      font-variant-numeric: tabular-nums;\n    }\n    .author {\n      min-width: 0;\n      white-space: nowrap;\n      overflow: hidden;\n      text-overflow: ellipsis;\n    }\n    .author a {\n      color: var(--ink);\n      text-decoration: none;\n    }\n    .author a:hover { text-decoration: underline; }\n    .subtle-link {\n      margin-left: 7px;\n      color: var(--accent);\n      font-size: 11px;\n      text-decoration: none;\n    }\n    .metric {\n      color: var(--muted);\n      font-variant-numeric: tabular-nums;\n      text-align: right;\n      white-space: nowrap;\n    }\n    .chart-cell {\n      min-width: 0;\n      display: flex;\n      align-items: center;\n      justify-content: flex-end;\n      padding-right: var(--chart-pad-r);\n    }\n    .chart {\n      display: grid;\n      grid-template-columns: repeat(41, var(--year-w));\n      align-items: end;\n      height: var(--chart-h);\n      gap: 2px;\n      width: calc((41 * var(--year-w)) + (40 * 2px));\n    }\n    .bar {\n      width: 100%;\n      min-height: 1px;\n      background: var(--bar);\n      border-radius: 2px 2px 0 0;\n    }\n    .bar.zero {\n      background: var(--bar-muted);\n      opacity: .45;\n    }\n    .missing {\n      justify-content: flex-end;\n      color: var(--missing);\n      font-size: 12px;\n      font-style: italic;\n    }\n    .axis {\n      display: grid;\n      grid-template-columns: repeat(41, var(--year-w));\n      gap: 2px;\n      justify-self: end;\n      margin-right: var(--chart-pad-r);\n      width: calc((41 * var(--year-w)) + (40 * 2px));\n      color: var(--muted);\n      font-size: 10px;\n      font-variant-numeric: tabular-nums;\n    }\n    .axis span {\n      transform: rotate(-45deg);\n      transform-origin: 100% 50%;\n      text-align: right;\n      height: 18px;\n      white-space: nowrap;\n    }\n    .axis span:not(.tick) { color: transparent; }\n    .empty {\n      display: none;\n      padding: 28px;\n      text-align: center;\n      color: var(--muted);\n      background: var(--panel);\n      border: 1px solid var(--line);\n      border-radius: 8px;\n    }\n    .empty.visible { display: block; }\n    @media (max-width: 860px) {\n      :root { --label-w: 210px; --citations-w: 78px; --h-index-w: 48px; --year-w: 9px; }\n      .controls { grid-template-columns: 1fr; }\n      .summary { justify-self: start; }\n      main { overflow-x: auto; }\n    }\n  </style>\n</head>\n<body>\n  <header>\n    <div class="topbar">\n      <h1>ACM Fellow Citation Timelines</h1>\n      <div class="controls">\n        <input id="search" type="search" placeholder="Search author" autocomplete="off">\n        <label class="toggle"><input id="showMissing" type="checkbox"> Show missing Scholar data</label>\n        <div id="summary" class="summary"></div>\n      </div>\n    </div>\n  </header>\n  <main>\n    <div id="table" class="table" aria-live="polite"></div>\n    <div id="empty" class="empty">No rows match the current filters.</div>\n  </main>\n  <script>\n    const DATA = __DATA_JSON__;\n    const YEAR_MIN = DATA.metadata.yearMin;\n    const YEAR_MAX = DATA.metadata.yearMax;\n    const YEARS = d3.range(YEAR_MIN, YEAR_MAX + 1).map(String);\n    const state = { query: \'\', showMissing: false };\n\n    const table = d3.select(\'#table\');\n    const summary = d3.select(\'#summary\');\n    const empty = d3.select(\'#empty\');\n\n    d3.select(\'#search\').on(\'input\', event => { state.query = event.target.value.trim().toLowerCase(); render(); });\n    d3.select(\'#showMissing\').on(\'change\', event => { state.showMissing = event.target.checked; render(); });\n    function fmt(value) {\n      return value == null ? \'\' : d3.format(\',\')(value);\n    }\n\n    function filteredRows() {\n      return DATA.rows.filter(row => {\n        if (!state.showMissing && !row.hasScholar) return false;\n        if (!state.query) return true;\n        return row.name.toLowerCase().includes(state.query);\n      });\n    }\n\n    function chart(row) {\n      if (!row.hasScholar) return \'<div class="chart-cell missing">No Scholar data</div>\';\n      const values = YEARS.map(year => row.citationByYear[year] || 0);\n      const max = d3.max(values) || 1;\n      const bars = YEARS.map((year, index) => {\n        const value = values[index];\n        const height = value ? Math.max(2, Math.round((value / max) * 100)) : 1;\n        const cls = value ? \'bar\' : \'bar zero\';\n        return `<div class="${cls}" style="height:${height}%" title="${year}: ${fmt(value)} citations"></div>`;\n      }).join(\'\');\n      return `<div class="chart-cell"><div class="chart" aria-label="Citation history for ${escapeHtml(row.name)}">${bars}</div></div>`;\n    }\n\n    function escapeHtml(value) {\n      return String(value).replace(/[&<>"\']/g, char => ({\'&\':\'&amp;\',\'<\':\'&lt;\',\'>\':\'&gt;\',\'"\':\'&quot;\',"\'":\'&#39;\'}[char]));\n    }\n\n    function authorCell(row) {\n      const name = escapeHtml(row.name);\n      const acm = row.acmProfile ? `<a href="${row.acmProfile}">${name}</a>` : name;\n      const scholar = row.hasScholar ? `<a class="subtle-link" href="${row.scholarProfile}">Scholar</a>` : \'\';\n      return `${acm}${scholar}`;\n    }\n\n    function citationsCell(row) {\n      return row.hasScholar ? fmt(row.citations) : \'\';\n    }\n\n    function hIndexCell(row) {\n      return row.hasScholar ? fmt(row.hIndex) : \'\';\n    }\n\n    function axisHtml() {\n      return `<div></div><div>Author</div><div>Citations</div><div>h-index</div><div></div>`;\n    }\n\n    function render() {\n      const rows = filteredRows();\n      const visibleWithData = rows.filter(row => row.hasScholar).length;\n      summary.text(`${fmt(rows.length)} shown · ${fmt(visibleWithData)} with Scholar data · ${YEAR_MIN}–${YEAR_MAX}`);\n      empty.classed(\'visible\', rows.length === 0);\n      table.style(\'display\', rows.length ? null : \'none\');\n\n      const html = [`<div class="row head">${axisHtml()}</div>`].concat(rows.map(row => `\n        <div class="row">\n          <div class="year">${row.year || \'\'}</div>\n          <div class="author" title="${escapeHtml(row.name)}">${authorCell(row)}</div>\n          <div class="metric">${citationsCell(row)}</div>\n          <div class="metric">${hIndexCell(row)}</div>\n          ${chart(row)}\n        </div>`)).join(\'\');\n      table.html(html);\n    }\n\n    render();\n  </script>\n</body>\n</html>\n'

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--acm", type=Path, default=DEFAULT_ACM, help="Path to data/acm_fellows.csv.")
    parser.add_argument("--scholar", type=Path, default=DEFAULT_SCHOLAR, help="Path to data/google_scholar_profiles.csv.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="HTML output path.")
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def int_or_none(value: str) -> int | None:
    value = (value or "").strip()
    return int(value) if value else None


def build_data(acm_rows: list[dict[str, str]], scholar_rows: list[dict[str, str]]) -> dict[str, Any]:
    scholar_by_profile = {row["profile"]: row for row in scholar_rows if row.get("profile")}
    rows: list[dict[str, Any]] = []
    years: set[int] = set()

    for acm in acm_rows:
        profile = acm.get("google_scholar_profile", "").strip()
        scholar = scholar_by_profile.get(profile) if profile else None
        citation_by_year: dict[str, int] = {}
        if scholar and scholar.get("citation_by_year"):
            citation_by_year = {str(year): int(count) for year, count in json.loads(scholar["citation_by_year"]).items()}
            years.update(int(year) for year in citation_by_year)

        rows.append(
            {
                "name": acm.get("name", ""),
                "year": int_or_none(acm.get("year", "")),
                "location": acm.get("location", ""),
                "acmProfile": acm.get("acm_fellow_profile", ""),
                "scholarProfile": profile,
                "hasScholar": bool(scholar and citation_by_year),
                "citations": int_or_none(scholar.get("citations", "") if scholar else ""),
                "hIndex": int_or_none(scholar.get("h_index", "") if scholar else ""),
                "firstCitationYear": int_or_none(scholar.get("first_citation_year", "") if scholar else ""),
                "citationByYear": citation_by_year,
            }
        )

    rows.sort(key=lambda row: (-(row["year"] or 0), row["name"].lower()))
    if not years:
        raise ValueError("No citation-by-year data found")

    return {
        "metadata": {
            "totalRows": len(rows),
            "joinedRows": sum(1 for row in rows if row["hasScholar"]),
            "missingRows": sum(1 for row in rows if not row["hasScholar"]),
            "yearMin": min(years),
            "yearMax": max(years),
        },
        "rows": rows,
    }


def render_html(data: dict[str, Any]) -> str:
    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return HTML_TEMPLATE.replace("__DATA_JSON__", data_json)


def main() -> int:
    args = parse_args()
    data = build_data(read_csv(args.acm), read_csv(args.scholar))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_html(data), encoding="utf-8")
    print(
        f"Wrote {args.output} rows={data['metadata']['totalRows']} "
        f"joined={data['metadata']['joinedRows']} missing={data['metadata']['missingRows']} "
        f"years={data['metadata']['yearMin']}-{data['metadata']['yearMax']}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
