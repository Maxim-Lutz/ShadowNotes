
```markdown
# ShadowNotes

ShadowNotes is a simple, encrypted note-taking application built in Python. It offers two versions for managing your notes securely:
- A **Command-Line Interface (CLI)** version.
- A **Graphical User Interface (GUI)** version (built with Tkinter).

Both versions use AES-256 GCM for secure, authenticated encryption and support custom note filenames, tagging, and various note operations such as adding, reading, editing, deleting, searching, exporting, importing, and changing note passwords.

## Features

- **Secure Encryption:** Uses AES-256 GCM for authenticated encryption.
- **Dual Interfaces:** Choose between a CLI version and a GUI version.
- **Custom Note Filenames:** Specify your own filename when adding a note; if omitted, a timestamp-based name is used.
- **Tagging & JSON Format:** Notes are stored as JSON objects (with content and tags) before encryption.
- **Note Operations:** Add, read, edit, delete, and search notes.
- **Export/Import:** Export decrypted notes to plaintext and import plaintext files as encrypted notes.
- **Change Password:** Update the encryption password for a note.

## Project Structure

```
ShadowNotes/
├── src/
│   ├── __init__.py        # Marks the src directory as a Python package
│   ├── config.py          # Configuration settings
│   ├── main.py            # CLI entry point
│   ├── gui.py             # GUI entry point (Tkinter)
│   ├── encryption.py      # Encryption and decryption functions (AES-256 GCM)
│   └── storage.py         # File operations for saving and loading notes
├── notes/                 # Directory for storing encrypted notes
├── tests/
│   ├── __init__.py        # Marks tests as a Python package
│   └── test_encryption.py # Unit tests for encryption functionality
├── build.py               # Build script to create executables (CLI and GUI)
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignore file
└── README.md              # Project documentation (this file)
```

## Requirements

- Python 3.x
- pip

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Maxim-Lutz/ShadowNotes.git
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

## Building the Executables

The project includes a build script that creates two separate executables:
- **CLI Version:** `ShadowNotes.exe` – a command-line version of the app.
- **GUI Version:** `ShadowNotesGui.exe` – a graphical version of the app built with Tkinter.

To build the executables, run the following command from the project root:
```sh
python build.py
```
This will create the executables in the `dist/` folder.

## Usage

### Running the CLI Version
Run the CLI executable (or run it via Python):
```sh
ShadowNotes.exe
```
The CLI version will prompt you for commands (e.g., add, read, edit, delete, list, search, etc.).

### Running the GUI Version
Run the GUI executable:
```sh
ShadowNotesGui.exe
```
This will open a graphical window where you can manage your notes interactively.

## License

ShadowNotes is open-source and released under the MIT License.
```
