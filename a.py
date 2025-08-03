import os

# Configuration
root_dir = r'/Users/noshinebnatadrita/Documents/naptagram/'  # Replace with your codebase root
output_file = 'full_codebase.txt'
include_extensions = ['.html', '.css', '.ipynb', '.py']  # Change as needed
exclude_dirs = {'node_modules', '__pycache__', 'nothing'}

with open(output_file, 'w', encoding='utf-8') as outfile:
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify dirnames in-place to skip excluded directories
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        for filename in filenames:
            if any(filename.endswith(ext) for ext in include_extensions):
                filepath = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(filepath, root_dir)
                outfile.write(f"\n\n# === {relative_path} ===\n\n")
                try:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"# [Could not read file: {e}]\n")
