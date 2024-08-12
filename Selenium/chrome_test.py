import os

# Check default paths
paths = [
    r"chromedriver-linux64.zip",
]

chrome_found = False
for path in paths:
    if os.path.exists(path):
        print(f"Chrome found at: {path}")
        chrome_found = True
        break

if not chrome_found:
    print("Chrome not found in default locations.")
