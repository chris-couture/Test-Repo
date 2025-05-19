import os

# Use raw string or forward slashes to avoid unicode escape issues
folder_path = r"C:\Users\YourName\Documents\markdown_files"

for filename in os.listdir(folder_path):
    if filename.endswith(".md"):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        inside_target_section = False
        skipping_blank_lines = False

        for line in lines:
            if line.strip() == "## Dictionary Terms and Weights":
                inside_target_section = True
                skipping_blank_lines = True
                new_lines.append(line)
                continue

            if inside_target_section:
                if skipping_blank_lines and line.strip() == "":
                    continue
                else:
                    skipping_blank_lines = False

            new_lines.append(line)

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

print("Done cleaning .md files.")
