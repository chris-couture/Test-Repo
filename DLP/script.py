import csv
import os

# === CONFIGURATION ===

csv_file = 'test.csv'  # Your CSV file name

output_folder = 'output_files'  # Folder to create files in

# Your markdown template
md_template = """# Title: {filename}

## Description

{description}

## Details

(Add details here.)

## Regex Value

{regex_value}
"""

# === SCRIPT ===

# Make sure the output folder exists
os.makedirs(output_folder, exist_ok=True)

with open(csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if not row or len(row) < 3:
            continue  # Skip empty rows or rows without enough columns
        filename = row[0].strip()
        description = row[1].strip()
        value = row[2].strip()

        if filename:
            # Sanitize filename and make sure it ends with .md
            safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()
            if not safe_filename.endswith('.md'):
                safe_filename += '.md'

            filepath = os.path.join(output_folder, safe_filename)

            # Populate the markdown template with the filename, description, and regex value
            file_title = os.path.splitext(safe_filename)[0]
            content = md_template.format(filename=file_title, description=description, regex_value=value)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

print(f"✅ Markdown files created successfully in folder: {output_folder}")
