import os

# Folder containing the .md files
folder_path = "path/to/your/md/files"  # ← Replace with your actual path

# Go through all .md files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".md"):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        inside_target_section = False
        skipping_blank_lines = False

        for i, line in enumerate(lines):
            if line.strip() == "## Dictionary Terms and Weights":
                inside_target_section = True
                skipping_blank_lines = True
                new_lines.append(line)
                continue

            if inside_target_section:
                if skipping_blank_lines and line.strip() == "":
                    continue  # skip blank line
                else:
                    skipping_blank_lines = False  # first non-blank line after header

            new_lines.append(line)

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

print("Done cleaning .md files.")
