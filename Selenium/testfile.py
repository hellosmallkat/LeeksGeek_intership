import os

file_path = r"/mnt/c/Users/Kat/Desktop/LeeksGeek/chromedriver-win64.zip"

# Check if the file exists
if os.path.exists(file_path):
    print(f"File '{file_path}' exists.")

    # Check if the script can read the file
    if os.access(file_path, os.R_OK):
        print(f"Script has read access to '{file_path}'.")
    else:
        print(f"Script does not have read access to '{file_path}'.")
else:
    print(f"File '{file_path}' does not exist.")
