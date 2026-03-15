import os

# List of files to delete
files_to_delete = ["intelligent_art.py", "art_generator.py"]

for file in files_to_delete:
    if os.path.exists(file):
        os.remove(file)
        print(f"Deleted {file}")
    else:
        print(f"{file} not found.")
