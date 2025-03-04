import subprocess
import os

def build_cli():
    command = [
        "pyinstaller",
        "--onefile",
        "--console",                # CLI version uses a console window
        "--name", "ShadowNotes",      # Name for the CLI executable
        "--paths=src",              # Include the src directory in the Python path
        "src/main.py"
    ]
    subprocess.run(command, check=True)

def build_gui():
    command = [
        "pyinstaller",
        "--onefile",
        "--windowed",               # GUI version: no console window
        "--name", "ShadowNotesGui",   # Name for the GUI executable
        "--paths=src",              # Include the src directory in the Python path
        "src/gui.py"
    ]
    subprocess.run(command, check=True)

def main():
    print("Building CLI version...")
    build_cli()
    print("Building GUI version...")
    build_gui()
    
    cli_exe = os.path.join("dist", "ShadowNotes.exe")
    gui_exe = os.path.join("dist", "ShadowNotesGui.exe")
    
    if os.path.exists(cli_exe):
        print("CLI Build complete. 'ShadowNotes.exe' has been created in the 'dist' folder.")
    else:
        print("CLI Build complete, but 'ShadowNotes.exe' was not found in the 'dist' folder.")
    
    if os.path.exists(gui_exe):
        print("GUI Build complete. 'ShadowNotesGui.exe' has been created in the 'dist' folder.")
    else:
        print("GUI Build complete, but 'ShadowNotesGui.exe' was not found in the 'dist' folder.")

if __name__ == "__main__":
    main()
