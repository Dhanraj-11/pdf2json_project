from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

styles = getSampleStyleSheet()
cell_style = styles["BodyText"]
cell_style.fontSize = 7
cell_style.leading = 9

headers = ["ID", "Date", "Company", "Rig", "What Was Seen", "What Was Discussed"]

data_rows = [
    ["92335", "06.08.2026", "Transocean", "TNG",
     "A person inside the accommodation area was not wearing the required PPE.",
     "I stopped the individual and reminded them of the PPE policy on site."],
    ["92336", "06.09.2026", "Noble Corp", "ND1",
     "Loose cable observed near the walkway on deck level 2.",
     "Reported to the supervisor and cable was secured immediately."],
    ["92337", "06.10.2026", "Valaris", "VAL-3",
     "Worker climbing ladder while carrying tools in both hands.",
     "Discussed three-point contact rule and proper tool transport."],
    ["92338", "06.11.2026", "Transocean", "TNG",
     "Housekeeping issue in the galley storage area.",
     "Area was cleaned and a reminder was sent to the catering team."],
]

table_data = [headers] + data_rows

# Wrap long text cells in Paragraph so they wrap instead of overflow
wrapped = []
for row in table_data:
    wrapped.append([Paragraph(str(c), cell_style) for c in row])

doc = SimpleDocTemplate("/home/claude/pdf2json_project/sample_report.pdf",
                         pagesize=landscape(A4),
                         leftMargin=1*cm, rightMargin=1*cm,
                         topMargin=1*cm, bottomMargin=1*cm)

col_widths = [1.5*cm, 2*cm, 3*cm, 2*cm, 8*cm, 8*cm]

t = Table(wrapped, colWidths=col_widths, repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("FONTSIZE", (0, 0), (-1, 0), 8),
]))

doc.build([t])
print("Sample PDF created.")
