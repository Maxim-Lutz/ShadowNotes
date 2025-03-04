import subprocess
import os

def main():
    command = [
        "pyinstaller",
        "--onefile",                # Bundle everything into a single executable
        # Do not use --windowed so a terminal opens
        "--name", "ShadowNotes",     # Output executable name
        "--paths=src",              # Include the src folder in the module search path
        "src/merged.py"             # Entry point: the merged launcher script
    ]
    subprocess.run(command, check=True)
    
    exe_path = os.path.join("dist", "ShadowNotes.exe")
    if os.path.exists(exe_path):
        print("Build complete: 'ShadowNotes.exe' created in the 'dist' folder.")
    else:
        print("Build complete, but 'ShadowNotes.exe' was not found in 'dist'.")

if __name__ == "__main__":
    main()
