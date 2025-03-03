import os
from datetime import datetime

# Define the directory for storing notes
NOTES_DIR = os.path.join(os.path.dirname(__file__), "../notes")
print("Notes directory:", NOTES_DIR)

if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)

def save_note(encrypted_data: bytes, custom_filename: str = None) -> str:
    if custom_filename:
        # If the filename does not end with .enc, add the extension
        if not custom_filename.endswith(".enc"):
            custom_filename += ".enc"
        filename = custom_filename
    else:
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".enc"
    filepath = os.path.join(NOTES_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(encrypted_data)
    return filename

def load_note(filename: str) -> bytes:
    filepath = os.path.join(NOTES_DIR, filename)
    with open(filepath, "rb") as f:
        return f.read()
