import subprocess
import os

def main():
    command = [
        "pyinstaller",
        "--onefile",
        "--console",
        "--name", "ShadowNotes",   # Sets the output executable name
        "--paths=src",             # Adds 'src' to the Python path
        "src/main.py"
    ]
    subprocess.run(command, check=True)
    exe_path = os.path.join("dist", "ShadowNotes.exe")
    if os.path.exists(exe_path):
        print("Build complete. ShadowNotes.exe has been created in the 'dist' folder.")
    else:
        print("Build complete, but ShadowNotes.exe was not found in the 'dist' folder.")

if __name__ == "__main__":
    main()
