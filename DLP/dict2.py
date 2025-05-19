import os

# Input and output folders
input_folder = r"C:\Users\YourName\Documents\markdown_files"
output_folder = r"C:\Users\YourName\Documents\markdown_cleaned"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop through all .md files
for filename in os.listdir(input_folder):
    if filename.endswith(".md"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with open(input_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        in_target_section = False
        skipping_blanks = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            if stripped == "## Dictionary Terms and Weights":
                in_target_section = True
                skipping_blanks = True
                new_lines.append(line)
                continue

            if in_target_section:
                if stripped == "":
                    continue  # Skip all blank lines
                else:
                    skipping_blanks = False
                    in_target_section = False  # Stop skipping once we hit non-blank content

            new_lines.append(line)

        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

print("Finished cleaning files. Output saved to:", output_folder)
