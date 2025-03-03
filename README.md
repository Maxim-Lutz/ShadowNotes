---
# ShadowNotes

ShadowNotes is a simple, encrypted note-taking application built in Python. It provides a command-line interactive interface for adding, reading, deleting, and listing encrypted notes. Notes are securely stored on your local machine, and you have the option to specify a custom file name when adding a note.

## Features

- **Encryption:** Uses AES encryption (via the cryptography library) to secure your notes.
- **Interactive CLI:** An easy-to-use command-line interface for managing notes.
- **Custom Note Filenames:** When adding a note, you can specify your own file name. If no custom name is provided, a default timestamp-based name is used.
- **Local Storage:** Notes are stored in an encrypted format in a dedicated folder.
- **Future Enhancements:** Plans include a GUI version, synchronization options, and mobile support.

## Project Structure

```
ShadowNotes/
├── src/                # Source code
│   ├── __init__.py     # Marks src as a Python module
│   ├── main.py         # Interactive CLI (entry point)
│   ├── encryption.py   # Encryption and decryption functions
│   ├── storage.py      # File operations (saving, loading, custom filenames)
│   └── config.py       # Configuration settings (optional)
├── notes/              # Directory for storing encrypted notes
├── tests/              # Unit tests
├── docs/               # Documentation
├── build.py            # Build script to create the executable
├── requirements.txt    # Python dependencies (e.g., cryptography)
├── setup.py            # Package setup file (if needed)
└── README.md           # This file
```

## Installation

### Requirements
- Python 3.x
- pip (Python package manager)

### Setup Steps
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/ShadowNotes.git
   cd ShadowNotes
   ```
2. **Create a virtual environment:**
   ```sh
   python -m venv venv
   ```
3. **Activate the virtual environment:**
   - **Windows:**
     ```sh
     venv\Scripts\activate
     ```
   - **Linux/macOS:**
     ```sh
     source venv/bin/activate
     ```
4. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Running the Application
Run the interactive CLI by executing:
```sh
python src/main.py
```
If you build the executable (see below), you can simply run the generated `ShadowNotes.exe`.

### Commands
Once the application starts, you can use the following commands:
- **add**: Add a new note.  
  The CLI will prompt you for:
  - Note content
  - A password (used to encrypt the note)
  - A custom filename (optional – if left blank, a default timestamp is used)
- **read**: Read an existing note by entering its filename.
- **delete**: Delete a note by specifying its filename.
- **list**: List all stored notes.
- **exit**: Exit the application.

## Building the Executable

You can create a standalone executable using PyInstaller. A build script is provided.

### Using the Build Script
1. Make sure your virtual environment is activated.
2. Run the build script:
   ```sh
   python build.py
   ```
   This script uses PyInstaller with the following options:
   - `--onefile`: Creates a single executable.
   - `--console`: Opens a console window.
   - `--name ShadowNotes`: Names the executable as ShadowNotes.exe.
   - `--paths=src`: Adds the src folder to the Python path.

The resulting executable will be placed in the `dist/` folder.

## License

ShadowNotes is open-source and released under the MIT License.

---

Feel free to contribute or provide feedback to help improve the project!