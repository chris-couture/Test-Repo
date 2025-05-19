import os

# Input and output folder paths (edit these)
input_folder = r"C:\Users\YourName\Documents\markdown_files"
output_folder = r"C:\Users\YourName\Documents\markdown_cleaned"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each .md file
for filename in os.listdir(input_folder):
    if filename.endswith(".md"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with open(input_path, "r", encoding="utf-8") as f:
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
                    continue  # Skip blank line
                else:
                    skipping_blank_lines = False

            new_lines.append(line)

        # Write cleaned content to new file in output folder
        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

print("All files cleaned and saved to:", output_folder)
