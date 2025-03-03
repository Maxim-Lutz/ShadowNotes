import subprocess

def main():
    command = [
        "pyinstaller",
        "--onefile",
        "--console",
        "--paths=src",  # Damit der src-Ordner im Suchpfad ist
        "src/main.py"
    ]
    subprocess.run(command, check=True)
    print("Build complete. Check the 'dist' folder for the executable.")

if __name__ == "__main__":
    main()
