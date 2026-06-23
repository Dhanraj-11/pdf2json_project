"""
pdf_to_json.py
--------------
Command-line tool: convert one or more PDFs (with tables) into JSON files.

Each output JSON file is saved with the SAME NAME as the input PDF
(just with .json instead of .pdf), in the same folder unless --output
is given.

USAGE
-----
  Single file:
      python pdf_to_json.py report.pdf

  Multiple files:
      python pdf_to_json.py report1.pdf report2.pdf report3.pdf

  Every PDF in a folder:
      python pdf_to_json.py --folder ./my_pdfs

  Choose where the JSON files go:
      python pdf_to_json.py --folder ./my_pdfs --output ./json_out

  Pretty vs compact JSON (pretty is default):
      python pdf_to_json.py report.pdf --compact
"""

import argparse
import json
import sys
from pathlib import Path

from converter import extract_tables_from_pdf


def convert_one(pdf_path: Path, output_dir: Path | None, pretty: bool) -> Path:
    rows = extract_tables_from_pdf(str(pdf_path))

    if output_dir is None:
        out_path = pdf_path.with_suffix(".json")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
        out_path = output_dir / (pdf_path.stem + ".json")

    with open(out_path, "w", encoding="utf-8") as f:
        if pretty:
            json.dump(rows, f, indent=2, ensure_ascii=False)
        else:
            json.dump(rows, f, ensure_ascii=False)

    return out_path, len(rows)


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF table(s) into a JSON file with the same name."
    )
    parser.add_argument(
        "pdfs", nargs="*", help="One or more PDF files to convert."
    )
    parser.add_argument(
        "--folder", help="Convert every .pdf file found in this folder."
    )
    parser.add_argument(
        "--output", help="Folder to save the .json file(s) into."
    )
    parser.add_argument(
        "--compact", action="store_true",
        help="Write compact JSON instead of pretty/indented JSON."
    )
    args = parser.parse_args()

    pdf_paths = [Path(p) for p in args.pdfs]

    if args.folder:
        folder = Path(args.folder)
        if not folder.is_dir():
            print(f"Folder not found: {folder}")
            sys.exit(1)
        pdf_paths += sorted(folder.glob("*.pdf"))

    if not pdf_paths:
        parser.print_help()
        sys.exit(1)

    output_dir = Path(args.output) if args.output else None

    print(f"Found {len(pdf_paths)} PDF file(s) to convert.\n")

    for pdf_path in pdf_paths:
        if not pdf_path.exists():
            print(f"  SKIPPED (not found): {pdf_path}")
            continue
        try:
            out_path, row_count = convert_one(pdf_path, output_dir, pretty=not args.compact)
            print(f"  OK   {pdf_path.name}  ->  {out_path}   ({row_count} rows)")
        except Exception as e:
            print(f"  FAIL {pdf_path.name}  ->  {e}")

    print("\nDone.")


if __name__ == "__main__":
    main()
