# pip install pandas openpyxl
import pandas as pd
import re
from openpyxl import load_workbook

EXCEL_PATH = "test.xlsx"
SHEET_NAME = "sheet1"
ID_COL = "Condition Number"
NAME_COL = "Content Classifier Name"

# --- 1) Read the Boolean logic from A1 ---
# header=None so row 1 is treated as data, usecols="A" to read only column A
logic_cell = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME, header=None, nrows=1, usecols="A")
boolean_logic = str(logic_cell.iat[0, 0])

# --- 2) Read the mapping table (headers are on row 2, so header=1) ---
df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME, header=1, usecols="A:B")
df = df.rename(columns=lambda c: str(c).strip())

# Keep rows that have both an ID and a Name
df = df[[ID_COL, NAME_COL]].dropna(subset=[ID_COL, NAME_COL])

def to_key(x):
    # Normalize numeric-like IDs to plain integer strings (e.g., 1.0 -> "1")
    s = str(x).strip()
    try:
        return str(int(float(s)))
    except:
        return s

mapping = {to_key(row[ID_COL]): str(row[NAME_COL]).strip()
           for _, row in df.iterrows()}

# --- 3) Replace whole-number tokens in the boolean expression ---
pattern = re.compile(r"\b\d+\b")

def replacer(m):
    num = m.group(0)
    return mapping.get(num, num)  # leave the number if it's not found

expanded_logic = pattern.sub(replacer, boolean_logic)

print("Original:", boolean_logic)
print("Expanded:", expanded_logic)

# --- 4) Write the expanded logic back to the workbook (B1 header, B2 value) ---
wb = load_workbook(EXCEL_PATH)
ws = wb[SHEET_NAME]
ws["B1"] = "Expanded Logic"
ws["B2"] = expanded_logic
wb.save(EXCEL_PATH)
