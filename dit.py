import os
import json


def list_files_json(startpath, output_file):
    root_dict = {}
    for root, dirs, files in os.walk(startpath):
        # Remove specific directories from traversal
        dirs[:] = [d for d in dirs if d not in ['.git', 'venv']]

        # Handle the relative pathing
        parts = root.replace(startpath, '').strip(os.sep).split(os.sep)
        current = root_dict
        for part in parts:
            current = current.setdefault(part, {})
        current['_files'] = files

    with open(output_file, 'w') as f:
        json.dump(root_dict, f, indent=4)


# Example usage:
directory_path = './'  # Change this to your directory path
output_file_path = 'directory_structure.json'  # Output file path
list_files_json(directory_path, output_file_path)
