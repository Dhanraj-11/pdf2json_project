# PDF Table → JSON Converter

A small command-line tool that takes any PDF containing a table and converts
it into a JSON file with the **same name** as the PDF.

Example: `ENGAGE_Report_09_06_2026.pdf` → `ENGAGE_Report_09_06_2026.json`

It works on **any** PDF that has a table, not just one specific report —
it automatically detects the header row and turns every row below it into
a JSON object.

---

## 1. Files in this project

```
pdf2json_project/
├── converter.py        # Core logic: extracts tables from a PDF
├── pdf_to_json.py       # Command-line tool you actually run
├── requirements.txt     # The one dependency this needs
├── sample_report.pdf     # A sample test file (table layout demo)
├── sample_report.json    # What the sample file converts to
└── README.md          # This file
```

You only need `converter.py`, `pdf_to_json.py`, and `requirements.txt` to use
the tool. The sample files are just there so you can confirm it works before
trying your own PDFs.

---

## 2. Setup on your laptop (one-time)

You need Python 3.9 or newer installed. Check with:

```bash
python3 --version
```

If that works, install the one dependency this project needs:

```bash
pip install -r requirements.txt
```

(On some systems you may need `pip3` instead of `pip`.)

That's it — setup is done.

---

## 3. How to use it

Open a terminal, `cd` into the project folder, then run one of these:

### Convert a single PDF
```bash
python pdf_to_json.py myreport.pdf
```
This creates `myreport.json` in the same folder.

### Convert several PDFs at once
```bash
python pdf_to_json.py report1.pdf report2.pdf report3.pdf
```

### Convert every PDF in a folder
```bash
python pdf_to_json.py --folder ./my_pdfs
```

### Save the JSON files somewhere else
```bash
python pdf_to_json.py --folder ./my_pdfs --output ./json_out
```

### Compact JSON (no indentation, smaller file)
```bash
python pdf_to_json.py myreport.pdf --compact
```

---

## 4. Try it right now with the included sample

```bash
python pdf_to_json.py sample_report.pdf
```

You should see:
```
Found 1 PDF file(s) to convert.

  OK   sample_report.pdf  ->  sample_report.json   (4 rows)

Done.
```

Open `sample_report.json` to see the result — that's exactly the format
your own converted reports will use.

---

## 5. What the output JSON looks like

```json
[
  {
    "id": "92335",
    "date": "06.08.2026",
    "company": "Transocean",
    "rig": "TNG",
    "what was seen": "A person inside the accommodation area was not wearing the required PPE.",
    "what was discussed": "I stopped the individual and reminded them of the PPE policy on site.",
    "_page": 1
  }
]
```

- Keys come straight from your PDF's table header row (lower-cased).
- `_page` tells you which PDF page that row came from.
- If a table repeats across multiple pages with the same header row, all
  rows are merged into one continuous list automatically.

---

## 6. If a PDF doesn't convert well

Most table PDFs work out of the box. If a particular PDF gives bad or empty
results, it's almost always one of these:

- **The PDF is a scanned image**, not real text (no real table grid for
  pdfplumber to detect). This needs OCR first, which this tool doesn't do.
- **The table has no visible lines/borders** and inconsistent spacing,
  making columns hard to detect automatically.

If you hit either case, send me the PDF and I'll add a customized rule
(or an OCR step) for that specific layout.

---

## 7. Why this works for "any new PDF"

`converter.py` doesn't hard-code any column names or file names. It:
1. Opens the PDF and scans every page for tables.
2. Detects whichever row is the header (first row of the first table found).
3. Turns every following row into a dict using those headers as keys.
4. If the same header repeats on later pages, it skips the duplicate header
   row and just keeps appending data — so multi-page reports come out as
   one clean JSON array.

So as long as your new PDF has a real table (lines or clearly aligned
columns), you can drop it in and run the same command — no code changes
needed.
