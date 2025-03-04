import os
import json
import hashlib
from encryption import encrypt_data, decrypt_data
from storage import save_note, load_note, NOTES_DIR

MASTER_FILE = "master.dat"
TODOS_FILE = "todos.enc"

def load_master_password_hash():
    if os.path.exists(MASTER_FILE):
        with open(MASTER_FILE, "r") as f:
            return f.read().strip()
    return None

def set_master_password():
    pwd = input("Set a master password for the app: ")
    confirm = input("Confirm master password: ")
    if pwd != confirm:
        print("Passwords do not match!")
        exit(1)
    hash_pwd = hashlib.sha256(pwd.encode()).hexdigest()
    with open(MASTER_FILE, "w") as f:
        f.write(hash_pwd)
    return pwd

def verify_master_password():
    stored = load_master_password_hash()
    if not stored:
        return set_master_password()
    pwd = input("Enter master password to unlock the app: ")
    if hashlib.sha256(pwd.encode()).hexdigest() == stored:
        return pwd
    else:
        print("Incorrect master password!")
        exit(1)

def todo_menu(master_password):
    # Load todos from TODOS_FILE (encrypted JSON array)
    if os.path.exists(TODOS_FILE):
        try:
            encrypted = open(TODOS_FILE, "rb").read()
            todos_json = decrypt_data(encrypted, master_password)
            todos = json.loads(todos_json.decode())
        except Exception as e:
            print("Error loading todos:", e)
            todos = []
    else:
        todos = []
    while True:
        sub = input("Todo Menu (add, list, done, delete, back): ").strip().lower()
        if sub == "back":
            break
        elif sub == "add":
            task = input("Enter new todo task: ")
            todos.append({"task": task, "done": False})
            print("Todo added.")
        elif sub == "list":
            if not todos:
                print("No todos found.")
            else:
                for i, t in enumerate(todos):
                    status = "Done" if t["done"] else "Pending"
                    print(f"{i}: {t['task']} [{status}]")
        elif sub == "done":
            index = input("Enter index of todo to mark as done: ")
            try:
                idx = int(index)
                todos[idx]["done"] = True
                print("Todo marked as done.")
            except Exception as e:
                print("Error:", e)
        elif sub == "delete":
            index = input("Enter index of todo to delete: ")
            try:
                idx = int(index)
                todos.pop(idx)
                print("Todo deleted.")
            except Exception as e:
                print("Error:", e)
        else:
            print("Unknown command.")
    # Save todos
    todos_json = json.dumps(todos).encode()
    encrypted_todos = encrypt_data(todos_json, master_password)
    with open(TODOS_FILE, "wb") as f:
        f.write(encrypted_todos)
    print("Todos saved.")

def main():
    master_password = verify_master_password()
    print("App unlocked.")
    print("Available commands: add, read, edit, delete, list, search, todo, exit")
    while True:
        command = input("Command: ").strip().lower()
        if command == "exit":
            break
        elif command == "add":
            note_content = input("Enter note content: ")
            password = input("Enter note password: ")
            custom_filename = input("Enter a custom filename (or leave blank for default): ").strip()
            if custom_filename == "":
                custom_filename = None
            tags_input = input("Enter tags (comma-separated, optional): ").strip()
            tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
            note_obj = {"content": note_content, "tags": tags}
            note_json = json.dumps(note_obj)
            encrypted = encrypt_data(note_json.encode(), password)
            filename = save_note(encrypted, custom_filename)
            print("Note saved as", filename)
        elif command == "read":
            filename = input("Enter filename to read: ")
            password = input("Enter note password: ")
            try:
                encrypted = load_note(filename)
                decrypted = decrypt_data(encrypted, password)
                try:
                    note_obj = json.loads(decrypted.decode())
                    print("Content:", note_obj.get("content", ""))
                    print("Tags:", ", ".join(note_obj.get("tags", [])))
                except json.JSONDecodeError:
                    print("Content:", decrypted.decode())
            except Exception as e:
                print("Error:", e)
        elif command == "edit":
            filename = input("Enter filename to edit: ")
            password = input("Enter note password: ")
            try:
                encrypted = load_note(filename)
                decrypted = decrypt_data(encrypted, password)
                try:
                    note_obj = json.loads(decrypted.decode())
                except json.JSONDecodeError:
                    note_obj = {"content": decrypted.decode(), "tags": []}
                print("Current content:", note_obj.get("content", ""))
                print("Current tags:", ", ".join(note_obj.get("tags", [])))
                new_content = input("Enter new content (leave blank to keep unchanged): ")
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
            password = input("Enter note password (assuming same for all notes): ")
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
        elif command == "todo":
            todo_menu(master_password)
        else:
            print("Unknown command.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
