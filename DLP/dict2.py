import os

# Input and output folders
input_folder = r"C:\Users\YourName\Documents\markdown_files"
output_folder = r"C:\Users\YourName\Documents\markdown_cleaned"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each .md file
for filename in os.listdir(input_folder):
    if filename.endswith(".md"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with open(input_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        in_cleanup_zone = False

        for line in lines:
            if line.strip() == "## Dictionary Terms and Weights":
                in_cleanup_zone = True
                new_lines.append(line)
                continue

            if in_cleanup_zone:
                # Skip blank lines entirely
                if line.strip() == "":
                    continue

            new_lines.append(line)

        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

print("All blank lines removed below '## Dictionary Terms and Weights'. Cleaned files saved to:", output_folder)
