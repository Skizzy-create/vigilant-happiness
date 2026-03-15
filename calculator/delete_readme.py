import os

# Remove the old README
if os.path.exists("README.md"):
    os.remove("README.md")
    print("README.md deleted.")
else:
    print("README.md not found.")
