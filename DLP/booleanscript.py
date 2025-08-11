# pip install openpyxl
import re
from openpyxl import load_workbook

EXCEL_PATH = "test.xlsx"
SHEET_NAME = "sheet1"

ID_HEADER = "Condition Number"
NAME_HEADER = "Content Classifier Name"

def normalize_id(x):
    """Make numeric-like IDs into plain int strings (e.g., '1.0' -> '1')."""
    if x is None:
        return ""
    s = str(x).strip()
    try:
        return str(int(float(s)))
    except:
        return s

# 1) Open workbook & sheet
wb = load_workbook(EXCEL_PATH)
ws = wb[SHEET_NAME]

# 2) Read original boolean logic from A1
original_logic = str(ws["A1"].value or "")

# 3) Find the header columns (row 2)
headers = { (ws.cell(row=2, column=c).value or "").strip(): c for c in range(1, ws.max_column + 1) }

if ID_HEADER not in headers or NAME_HEADER not in headers:
    raise KeyError(f"Could not find required headers '{ID_HEADER}' and/or '{NAME_HEADER}' in row 2. "
                   f"Found: {list(headers.keys())}")

id_col = headers[ID_HEADER]
name_col = headers[NAME_HEADER]

# 4) Build mapping dict from rows 3..N
mapping = {}
for r in range(3, ws.max_row + 1):
    id_val = ws.cell(row=r, column=id_col).value
    name_val = ws.cell(row=r, column=name_col).value
    if id_val is None or name_val is None:
        continue
    key = normalize_id(id_val)
    if key:
        mapping[key] = str(name_val).strip()

# 5) Replace whole-number tokens in the boolean expression
pattern = re.compile(r"\b\d+\b")

def replacer(m):
    tok = m.group(0)
    return mapping.get(tok, tok)

expanded_logic = pattern.sub(replacer, original_logic)

print("Original:", original_logic)
print("Expanded:", expanded_logic)

# 6) Write the result back to the sheet
ws["B1"] = "Expanded Logic"
ws["B2"] = expanded_logic
wb.save(EXCEL_PATH)
