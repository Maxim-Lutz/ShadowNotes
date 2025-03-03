import os
from encryption import encrypt_data, decrypt_data
from storage import save_note, load_note, NOTES_DIR

def main():
    print("Welcome to ShadowNotes Interactive CLI")
    print("Type 'help' to see available commands.\n")

    while True:
        command = input("Command (add, read, delete, list, exit): ").strip().lower()
        if command == "exit":
            break
        elif command == "help":
            print("Available commands: add, read, delete, list, exit")
        elif command == "add":
            note_content = input("Enter note content: ")
            password = input("Enter password: ")
            custom_filename = input("Enter a custom filename (or leave blank for default): ").strip()
            if custom_filename == "":
                custom_filename = None
            encrypted = encrypt_data(note_content.encode(), password)
            filename = save_note(encrypted, custom_filename)
            print("Note saved as", filename)
        elif command == "read":
            filename = input("Enter filename to read: ")
            password = input("Enter password: ")
            try:
                encrypted = load_note(filename)
                decrypted = decrypt_data(encrypted, password)
                print("\nNote content:")
                print(decrypted.decode(), "\n")
            except Exception as e:
                print("Error:", e)
        elif command == "delete":
            filename = input("Enter filename to delete: ")
            filepath = os.path.join(NOTES_DIR, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                print("Note deleted.")
            else:
                print("Note not found.")
        elif command == "list":
            files = os.listdir(NOTES_DIR)
            if files:
                print("Notes:")
                for f in files:
                    print(f)
            else:
                print("No notes found.")
        else:
            print("Unknown command. Type 'help' to see available commands.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
