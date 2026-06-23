"""
converter.py
------------
Core logic: read a PDF that contains a table, extract every row,
and return it as a list of dicts (one dict per row, keyed by header).

Works on ANY pdf as long as it has a real table grid OR consistent
whitespace-aligned columns that pdfplumber can detect. No filenames
or column names are hard-coded, so a new/different PDF layout will
still work as long as it has tabular data.
"""

import pdfplumber
import re


def _clean_cell(text):
    """Normalize a single cell's text: collapse newlines/extra spaces."""
    if text is None:
        return ""
    text = str(text).replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _make_unique_headers(headers):
    """
    Turn raw header cells into clean, unique, JSON-safe keys.
    Handles blank headers and duplicate headers (e.g. two "Notes" columns).
    """
    cleaned = []
    seen = {}
    for i, h in enumerate(headers):
        h = _clean_cell(h).lower()
        if not h:
            h = f"column_{i+1}"
        if h in seen:
            seen[h] += 1
            h = f"{h}_{seen[h]}"
        else:
            seen[h] = 0
        cleaned.append(h)
    return cleaned


def extract_tables_from_pdf(pdf_path, table_settings=None):
    """
    Extract all tables from a PDF.

    Returns a list of dicts, where each dict is one table row,
    e.g. {"id": "92335", "date": "06.08.2026", "company": "Transocean", ...}

    If the PDF has multiple tables across multiple pages that all share
    the same header row, they are merged into a single flat list — this
    matches reports like the ENGAGE report where the table repeats/continues
    across pages.
    """
    if table_settings is None:
        # Good general-purpose defaults; works for both ruled-line tables
        # and tables that only rely on text alignment.
        table_settings = {
            "vertical_strategy": "lines_strict",
            "horizontal_strategy": "lines_strict",
        }

    all_rows = []
    headers = None

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables(table_settings)

            # Fallback: if the strict line-based strategy finds nothing
            # on this page, retry with the more lenient text-based strategy.
            if not tables:
                tables = page.extract_tables({
                    "vertical_strategy": "text",
                    "horizontal_strategy": "text",
                })

            for table in tables:
                if not table or len(table) < 1:
                    continue

                first_row = [_clean_cell(c) for c in table[0]]

                # Decide if this table's first row is a header row.
                # Heuristic: if it matches the header we already locked in,
                # OR if we have no header yet, treat row 0 as the header.
                if headers is None:
                    headers = _make_unique_headers(first_row)
                    body_rows = table[1:]
                elif first_row == [h for h in first_row]:  # always true; kept for clarity
                    candidate_header = _make_unique_headers(first_row)
                    if candidate_header == headers:
                        # Repeated header row on a later page — skip it.
                        body_rows = table[1:]
                    else:
                        # Not a header repeat — treat all rows as data.
                        body_rows = table

                for row in body_rows:
                    cells = [_clean_cell(c) for c in row]
                    # Skip fully blank rows
                    if not any(cells):
                        continue
                    # Pad/truncate row to match header length
                    if len(cells) < len(headers):
                        cells += [""] * (len(headers) - len(cells))
                    elif len(cells) > len(headers):
                        cells = cells[: len(headers)]

                    row_dict = dict(zip(headers, cells))
                    row_dict["_page"] = page_num
                    all_rows.append(row_dict)

    return all_rows
