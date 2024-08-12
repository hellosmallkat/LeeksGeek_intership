import platform

os_type = platform.system()
print(f"Operating System: {os_type}")

if os_type == "Windows":
    print("You need the Windows version of ChromeDriver.")
elif os_type == "Linux":
    print("You need the Linux version of ChromeDriver.")
elif os_type == "Darwin":
    print("You need the macOS version of ChromeDriver.")
else:
    print("Unknown operating system.")
