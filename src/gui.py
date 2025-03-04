import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import json
import hashlib
from encryption import encrypt_data, decrypt_data
from storage import NOTES_DIR, save_note, load_note

MASTER_FILE = "master.dat"
TODOS_FILE = "todos.enc"

def load_master_password():
    try:
        with open(MASTER_FILE, "r") as f:
            return f.read().strip()
    except:
        return None

def set_master_password():
    pwd = simpledialog.askstring("Set Master Password", "Set a master password for the app:", show="*")
    confirm = simpledialog.askstring("Confirm Master Password", "Confirm master password:", show="*")
    if pwd != confirm:
        messagebox.showerror("Error", "Passwords do not match!")
        exit(1)
    hash_pwd = hashlib.sha256(pwd.encode()).hexdigest()
    with open(MASTER_FILE, "w") as f:
        f.write(hash_pwd)
    return pwd

def verify_master_password():
    stored = load_master_password()
    if not stored:
        return set_master_password()
    pwd = simpledialog.askstring("Master Password", "Enter master password to unlock the app:", show="*")
    if hashlib.sha256(pwd.encode()).hexdigest() == stored:
        return pwd
    else:
        messagebox.showerror("Error", "Incorrect master password!")
        exit(1)

class ShadowNotesGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.master_password = verify_master_password()
        self.title("ShadowNotes GUI")
        self.geometry("800x600")
        self.create_widgets()
        self.refresh_notes_list()

    def create_widgets(self):
        self.notes_listbox = tk.Listbox(self, width=40)
        self.notes_listbox.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.refresh_button = tk.Button(self.buttons_frame, text="Refresh List", command=self.refresh_notes_list)
        self.refresh_button.pack(pady=2)
        self.add_button = tk.Button(self.buttons_frame, text="Add Note", command=self.add_note)
        self.add_button.pack(pady=2)
        self.read_button = tk.Button(self.buttons_frame, text="Read Note", command=self.read_note)
        self.read_button.pack(pady=2)
        self.edit_button = tk.Button(self.buttons_frame, text="Edit Note", command=self.edit_note)
        self.edit_button.pack(pady=2)
        self.delete_button = tk.Button(self.buttons_frame, text="Delete Note", command=self.delete_note)
        self.delete_button.pack(pady=2)
        self.todo_button = tk.Button(self.buttons_frame, text="Todo", command=self.open_todo_window)
        self.todo_button.pack(pady=2)
        self.note_text = tk.Text(self, wrap=tk.WORD)
        self.note_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def refresh_notes_list(self):
        self.notes_listbox.delete(0, tk.END)
        files = os.listdir(NOTES_DIR)
        for f in files:
            self.notes_listbox.insert(tk.END, f)

    def add_note(self):
        note_content = simpledialog.askstring("Add Note", "Enter note content:")
        if note_content is None:
            return
        password = simpledialog.askstring("Note Password", "Enter password for the note:", show="*")
        if password is None:
            return
        custom_filename = simpledialog.askstring("Custom Filename", "Enter custom filename (optional):")
        tags_input = simpledialog.askstring("Tags", "Enter tags (comma-separated, optional):")
        tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
        note_obj = {"content": note_content, "tags": tags}
        note_json = json.dumps(note_obj)
        encrypted = encrypt_data(note_json.encode(), password)
        filename = save_note(encrypted, custom_filename)
        messagebox.showinfo("Success", f"Note saved as {filename}")
        self.refresh_notes_list()

    def read_note(self):
        selected = self.notes_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No note selected")
            return
        filename = self.notes_listbox.get(selected[0])
        password = simpledialog.askstring("Note Password", "Enter password for the note:", show="*")
        if password is None:
            return
        try:
            encrypted = load_note(filename)
            decrypted = decrypt_data(encrypted, password)
            try:
                note_obj = json.loads(decrypted.decode())
                content = note_obj.get("content", "")
                tags = note_obj.get("tags", [])
                display_text = f"Content:\n{content}\n\nTags: {', '.join(tags)}"
            except json.JSONDecodeError:
                display_text = decrypted.decode()
            self.note_text.delete(1.0, tk.END)
            self.note_text.insert(tk.END, display_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def edit_note(self):
        selected = self.notes_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No note selected")
            return
        filename = self.notes_listbox.get(selected[0])
        password = simpledialog.askstring("Note Password", "Enter password for the note:", show="*")
        if password is None:
            return
        try:
            encrypted = load_note(filename)
            decrypted = decrypt_data(encrypted, password)
            try:
                note_obj = json.loads(decrypted.decode())
            except json.JSONDecodeError:
                note_obj = {"content": decrypted.decode(), "tags": []}
            current_content = note_obj.get("content", "")
            current_tags = note_obj.get("tags", [])
            new_content = simpledialog.askstring("Edit Note", "Enter new content (leave blank to keep unchanged):", initialvalue=current_content)
            new_tags = simpledialog.askstring("Edit Tags", "Enter new tags (comma-separated, leave blank to keep unchanged):", initialvalue=", ".join(current_tags))
            if new_content:
                note_obj["content"] = new_content
            if new_tags:
                note_obj["tags"] = [tag.strip() for tag in new_tags.split(",")]
            new_note_json = json.dumps(note_obj)
            new_encrypted = encrypt_data(new_note_json.encode(), password)
            filepath = os.path.join(NOTES_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(new_encrypted)
            messagebox.showinfo("Success", "Note updated")
            self.refresh_notes_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_note(self):
        selected = self.notes_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No note selected")
            return
        filename = self.notes_listbox.get(selected[0])
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {filename}?")
        if confirm:
            filepath = os.path.join(NOTES_DIR, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                messagebox.showinfo("Deleted", "Note deleted")
                self.refresh_notes_list()
            else:
                messagebox.showerror("Error", "Note not found")

    def open_todo_window(self):
        # Load todos from TODOS_FILE
        if os.path.exists(TODOS_FILE):
            try:
                with open(TODOS_FILE, "rb") as f:
                    encrypted_todos = f.read()
                todos_json = decrypt_data(encrypted_todos, self.master_password)
                todos = json.loads(todos_json.decode())
            except Exception as e:
                messagebox.showerror("Error", f"Error loading todos: {e}")
                todos = []
        else:
            todos = []
        todo_win = tk.Toplevel(self)
        todo_win.title("Todo List")
        todo_win.geometry("400x300")
        listbox = tk.Listbox(todo_win)
        listbox.pack(fill=tk.BOTH, expand=True)
        for i, t in enumerate(todos):
            status = "Done" if t["done"] else "Pending"
            listbox.insert(tk.END, f"{i}: {t['task']} [{status}]")
        def add_task():
            task = simpledialog.askstring("New Task", "Enter new todo task:", parent=todo_win)
            if task:
                todos.append({"task": task, "done": False})
                listbox.insert(tk.END, f"{len(todos)-1}: {task} [Pending]")
        def mark_done():
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                todos[idx]["done"] = True
                listbox.delete(idx)
                status = "Done"
                listbox.insert(idx, f"{idx}: {todos[idx]['task']} [{status}]")
        def delete_task():
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                listbox.delete(idx)
                todos.pop(idx)
                listbox.delete(0, tk.END)
                for i, t in enumerate(todos):
                    status = "Done" if t["done"] else "Pending"
                    listbox.insert(tk.END, f"{i}: {t['task']} [{status}]")
        add_btn = tk.Button(todo_win, text="Add Task", command=add_task)
        add_btn.pack(side=tk.LEFT, padx=5, pady=5)
        done_btn = tk.Button(todo_win, text="Mark Done", command=mark_done)
        done_btn.pack(side=tk.LEFT, padx=5, pady=5)
        delete_btn = tk.Button(todo_win, text="Delete Task", command=delete_task)
        delete_btn.pack(side=tk.LEFT, padx=5, pady=5)
        def save_todos():
            try:
                todos_json = json.dumps(todos).encode()
                encrypted_todos = encrypt_data(todos_json, self.master_password)
                with open(TODOS_FILE, "wb") as f:
                    f.write(encrypted_todos)
                messagebox.showinfo("Success", "Todos saved.")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving todos: {e}")
        save_btn = tk.Button(todo_win, text="Save Todos", command=save_todos)
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)

if __name__ == "__main__":
    app = ShadowNotesGUI()
    app.mainloop()
