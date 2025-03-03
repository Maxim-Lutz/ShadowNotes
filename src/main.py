import os
import json
from encryption import encrypt_data, decrypt_data
from storage import save_note, load_note, NOTES_DIR

def main():
    print("Welcome to ShadowNotes Interactive CLI")
    print("Type 'help' to see available commands.\n")

    while True:
        command = input("Command (add, read, edit, delete, list, search, export, import, change, exit): ").strip().lower()
        if command == "exit":
            break
        elif command == "help":
            print("Available commands: add, read, edit, delete, list, search, export, import, change, exit")
        elif command == "add":
            note_content = input("Enter note content: ")
            password = input("Enter password: ")
            custom_filename = input("Enter a custom filename (or leave blank for default): ").strip()
            if custom_filename == "":
                custom_filename = None
            tags_input = input("Enter tags (comma-separated, optional): ").strip()
            tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
            note_obj = {
                "content": note_content,
                "tags": tags
            }
            note_json = json.dumps(note_obj)
            encrypted = encrypt_data(note_json.encode(), password)
            filename = save_note(encrypted, custom_filename)
            print("Note saved as", filename)
        elif command == "read":
            filename = input("Enter filename to read: ")
            password = input("Enter password: ")
            try:
                encrypted = load_note(filename)
                decrypted = decrypt_data(encrypted, password)
                try:
                    note_obj = json.loads(decrypted.decode())
                    print("\nNote content:")
                    print(note_obj.get("content", ""))
                    print("Tags:", ", ".join(note_obj.get("tags", [])))
                except json.JSONDecodeError:
                    print("\nNote content:")
                    print(decrypted.decode(), "\n")
            except Exception as e:
                print("Error:", e)
        elif command == "edit":
            filename = input("Enter filename to edit: ")
            password = input("Enter password: ")
            try:
                encrypted = load_note(filename)
                decrypted = decrypt_data(encrypted, password)
                try:
                    note_obj = json.loads(decrypted.decode())
                    current_content = note_obj.get("content", "")
                    current_tags = note_obj.get("tags", [])
                except json.JSONDecodeError:
                    current_content = decrypted.decode()
                    current_tags = []
                    note_obj = {"content": current_content, "tags": current_tags}
                print("\nCurrent note content:")
                print(current_content)
                print("Current tags:", ", ".join(current_tags))
                new_content = input("\nEnter new content (leave blank to keep unchanged): ")
                new_tags_input = input("Enter new tags (comma-separated, leave blank to keep unchanged): ").strip()
                if new_content:
                    note_obj["content"] = new_content
                if new_tags_input:
                    note_obj["tags"] = [tag.strip() for tag in new_tags_input.split(",")]
                new_note_json = json.dumps(note_obj)
                new_encrypted = encrypt_data(new_note_json.encode(), password)
                filepath = os.path.join(NOTES_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(new_encrypted)
                print("Note updated.")
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
        elif command == "search":
            search_term = input("Enter keyword to search: ").strip().lower()
            password = input("Enter password (assuming same for all notes): ")
            found = False
            for f in os.listdir(NOTES_DIR):
                try:
                    encrypted = load_note(f)
                    decrypted = decrypt_data(encrypted, password)
                    try:
                        note_obj = json.loads(decrypted.decode())
                        content = note_obj.get("content", "").lower()
                        tags = " ".join(note_obj.get("tags", [])).lower()
                    except json.JSONDecodeError:
                        content = decrypted.decode().lower()
                        tags = ""
                    if search_term in content or search_term in tags:
                        print("Match found in:", f)
                        found = True
                except Exception:
                    continue
            if not found:
                print("No matches found.")
        elif command == "export":
            # Export a note's content to a plaintext file
            note_filename = input("Enter note filename to export: ")
            export_filename = input("Enter export filename (e.g., note.md): ").strip()
            password = input("Enter password: ")
            try:
                encrypted = load_note(note_filename)
                decrypted = decrypt_data(encrypted, password)
                try:
                    note_obj = json.loads(decrypted.decode())
                    content = note_obj.get("content", "")
                except json.JSONDecodeError:
                    content = decrypted.decode()
                with open(export_filename, "w", encoding="utf-8") as f:
                    f.write(content)
                print("Note exported to", export_filename)
            except Exception as e:
                print("Error:", e)
        elif command == "import":
            # Import a plaintext file as a new encrypted note
            import_filename = input("Enter plaintext filename to import: ").strip()
            try:
                with open(import_filename, "r", encoding="utf-8") as f:
                    content = f.read()
                password = input("Enter password to encrypt the note: ")
                custom_filename = input("Enter a custom filename (or leave blank for default): ").strip()
                if custom_filename == "":
                    custom_filename = None
                tags_input = input("Enter tags (comma-separated, optional): ").strip()
                tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
                note_obj = {
                    "content": content,
                    "tags": tags
                }
                note_json = json.dumps(note_obj)
                encrypted = encrypt_data(note_json.encode(), password)
                filename = save_note(encrypted, custom_filename)
                print("Note imported and saved as", filename)
            except Exception as e:
                print("Error:", e)
        elif command == "change":
            # Change the password for a note
            filename = input("Enter filename to change password: ")
            current_password = input("Enter current password: ")
            try:
                encrypted = load_note(filename)
                decrypted = decrypt_data(encrypted, current_password)
                new_password = input("Enter new password: ")
                # Re-encrypt using the new password
                new_encrypted = encrypt_data(decrypted, new_password)
                filepath = os.path.join(NOTES_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(new_encrypted)
                print("Password changed for note", filename)
            except Exception as e:
                print("Error:", e)
        else:
            print("Unknown command. Type 'help' to see available commands.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
