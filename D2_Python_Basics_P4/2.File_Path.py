import os

# 1. Get the Current Working Directory (CWD)
cwd = os.getcwd()
print(f"I am running from: {cwd}")

# 2. List all files in a folder
files = os.listdir('.') # '.' means current folder
print(f"Files here: {files}")

# 3. Join paths (CRITICAL: Do not use '+' to join paths)
# This handles the different slashes for Windows (\) vs Linux (/) automatically.
data_path = os.path.join(cwd, "datasets", "train.csv")

from pathlib import Path

# 1. Get the path of the current file
# __file__ is a special variable for the script you are running
current_file = Path(__file__).resolve()
print(f"This script is at: {current_file}")

# 2. Get the parent directory (Folder containing the script)
project_root = current_file.parent
print(f"Project root: {project_root}")

# 3. Accessing subfolders (The '/' operator is overloaded here)
data_folder = project_root / "1.lambda.md" 
print(f"Data folder exists? {data_folder.exists()}")