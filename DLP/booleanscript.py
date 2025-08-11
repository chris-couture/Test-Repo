# pip install pandas openpyxl
import pandas as pd
import re
from openpyxl import load_workbook
from pathlib import Path

# --- Config tailored to your sheet ---
EXCEL_PATH = "test.xlsx"
SHEET_NAME = "sheet1"
ID_COL = "Condition Number"
NAME_COL = "Content Classifier Name"
TYPE_COL = "Type"
THRESH_COL = "Threshold"
OUTPUT_MD = "dlp_output.md"

# --- Helpers ---
def normalize_id(x):
    """Normalize numeric-like IDs to plain integer strings (e.g., 1.0 -> '1')."""
    s = str(x).strip()
    try:
        return str(int(float(s)))
    except:
        return s

def escape_md_cell(text):
    """Escape pipe characters in Markdown cell content."""
    return str(text).replace("|", r"\|")

def df_to_markdown(df):
    """Render a pandas DataFrame to a Markdown table without extra deps."""
    cols = list(df.columns)
    header = "| " + " | ".join(escape_md_cell(c) for c in cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    rows = []
    for _, row in df.iterrows():
        cells = [escape_md_cell(row[c]) for c in cols]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep] + rows)

# --- 1) Read the Boolean logic from A1 ---
logic_cell = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME, header=None, nrows=1, usecols="A")
original_logic = str(logic_cell.iat[0, 0])

# --- 2) Read the mapping table (headers are on row 2, so header=1) ---
df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME, header=1, usecols="A:D")
# Normalize header names just in case
df = df.rename(columns=lambda c: str(c).strip())

# Keep/rename only the columns we care about, in the desired order
df = df[[ID_COL, NAME_COL, TYPE_COL, THRESH_COL]].copy()

# Drop rows with no ID or no Name
df = df.dropna(subset=[ID_COL, NAME_COL])

# Normalize IDs to strings like '1', '2', ...
df[ID_COL] = df[ID_COL].apply(normalize_id)
df[NAME_COL] = df[NAME_COL].astype(str)
df[TYPE_COL] = df[TYPE_COL].astype(str)
df[THRESH_COL] = df[THRESH_COL].astype(str)

# Build mapping for replacement
mapping = dict(zip(df[ID_COL], df[NAME_COL]))

# --- 3) Replace whole-number tokens in the boolean expression ---
token_pattern = re.compile(r"\b\d+\b")

def replacer(m):
    num = m.group(0)
    return mapping.get(num, num)  # leave the number if not found

expanded_logic = token_pattern.sub(replacer, original_logic)

# --- 4) Build Markdown content ---
md_lines = []

# Section: Full input table first (as requested)
md_lines.append("# DLP Classifier Logic Expansion")
md_lines.append("")
md_lines.append("## Input Classifiers (from Excel)")
md_lines.append("")
md_lines.append(df_to_markdown(df))
md_lines.append("")

# Section: Original logic
md_lines.append("## Original Boolean Logic (cell A1)")
md_lines.append("")
md_lines.append("```")
md_lines.append(original_logic)
md_lines.append("```")
md_lines.append("")

# Section: Expanded logic (at the bottom)
md_lines.append("## Expanded Boolean Logic (by classifier name)")
md_lines.append("")
md_lines.append("```")
md_lines.append(expanded_logic)
md_lines.append("```")
md_lines.append("")

# Optionally, warn if any IDs in the logic were not found in the table
ids_in_logic = set(token_pattern.findall(original_logic))
missing = sorted(i for i in ids_in_logic if i not in mapping)
if missing:
    md_lines.append("> **Note:** The following condition numbers were referenced in the logic but not found in the table: " + ", ".join(missing))
    md_lines.append("")

# --- 5) Write Markdown file ---
Path(OUTPUT_MD).write_text("\n".join(md_lines), encoding="utf-8")

print(f"Wrote {OUTPUT_MD}")
