import sys, json, os
import pdfplumber

def clean(text):
    if not text:
        return ""
    return " ".join(text.replace("\n", " ").split()).strip()

def convert(pdf_path, json_path):
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    if not row or not row[0]:
                        continue
                    try:
                        rid = int(row[0])
                    except:
                        continue
                    rows.append({
                        "id": rid,
                        "date": clean(row[1]) if len(row)>1 else "",
                        "company": clean(row[2]) if len(row)>2 else "",
                        "rig": clean(row[3]) if len(row)>3 else "",
                        "whatWasSeen": clean(row[4]) if len(row)>4 else "",
                        "whatWasDiscussed": clean(row[5]) if len(row)>5 else "",
                        "whatWasReinforced": clean(row[6]) if len(row)>6 else "",
                        "commentsAddedByRigLeadership": clean(row[7]) if len(row)>7 else "",
                    })
    rows.sort(key=lambda x: x["id"])
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    return len(rows)

pdf_path = sys.argv[1]
json_path = os.path.splitext(pdf_path)[0] + ".json"
count = convert(pdf_path, json_path)
print(f"Done! {count} records saved to {json_path}")