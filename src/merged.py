import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import os, json, hashlib
from encryption import encrypt_data, decrypt_data
from storage import save_note, load_note, NOTES_DIR

# Define user data directory for storing master password and todos
USER_DATA_DIR = os.path.join(os.path.expanduser("~"), ".ShadowNotes")
if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)
MASTER_FILE = os.path.join(USER_DATA_DIR, "master.dat")
TODOS_FILE = os.path.join(USER_DATA_DIR, "todos.enc")

def load_master_password_hash():
    if os.path.exists(MASTER_FILE):
        with open(MASTER_FILE, "r") as f:
            return f.read().strip()
    return None

def set_master_password():
    pwd = simpledialog.askstring("Set Master Password", "Set a master password for the app:", show="*")
    confirm = simpledialog.askstring("Confirm Master Password", "Confirm master password:", show="*")
    if pwd != confirm:
        messagebox.showerror("Error", "Passwords do not match!")
        return None
    hash_pwd = hashlib.sha256(pwd.encode()).hexdigest()
    with open(MASTER_FILE, "w") as f:
        f.write(hash_pwd)
    return pwd

def verify_master_password():
    stored = load_master_password_hash()
    if not stored:
        pwd = set_master_password()
        if pwd is None:
            exit(1)
        return pwd
    pwd = simpledialog.askstring("Master Password", "Enter master password to unlock the app:", show="*")
    if hashlib.sha256(pwd.encode()).hexdigest() == stored:
        return pwd
    else:
        messagebox.showerror("Error", "Incorrect master password!")
        exit(1)

# --- CLI Interface embedded in Tkinter ---
class CLIFrame(tk.Frame):
    def __init__(self, master, master_password):
        super().__init__(master)
        self.master_password = master_password
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.print_output("CLI Mode Activated. Type 'help' for commands.\n")
        
    def create_widgets(self):
        self.output_text = tk.Text(self, wrap=tk.WORD, height=20)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.input_entry = tk.Entry(self)
        self.input_entry.pack(fill=tk.X)
        self.input_entry.bind("<Return>", self.handle_command)
    
    def print_output(self, text):
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
    
    def handle_command(self, event):
        command = self.input_entry.get().strip()
        self.print_output("> " + command + "\n")
        self.input_entry.delete(0, tk.END)
        self.process_command(command)
    
    def process_command(self, command):
        if command == "help":
            self.print_output("Commands: add, read, edit, delete, list, search, todo, exit\n")
        elif command == "exit":
            self.master.destroy()
        elif command == "list":
            files = os.listdir(NOTES_DIR)
            if files:
                self.print_output("Notes:\n")
                for f in files:
                    self.print_output(f + "\n")
            else:
                self.print_output("No notes found.\n")
        elif command.startswith("add"):
            note_content = simpledialog.askstring("Add Note", "Enter note content:")
            if note_content is None: return
            note_password = simpledialog.askstring("Note Password", "Enter password for the note:", show="*")
            if note_password is None: return
            custom_filename = simpledialog.askstring("Custom Filename", "Enter custom filename (optional):")
            tags_input = simpledialog.askstring("Tags", "Enter tags (comma-separated, optional):")
            tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
            note_obj = {"content": note_content, "tags": tags}
            note_json = json.dumps(note_obj)
            encrypted = encrypt_data(note_json.encode(), note_password)
            filename = save_note(encrypted, custom_filename)
            self.print_output("Note saved as " + filename + "\n")
        elif command.startswith("read"):
            filename = simpledialog.askstring("Read Note", "Enter filename to read:")
            if not filename: return
            note_password = simpledialog.askstring("Note Password", "Enter note password:", show="*")
            try:
                encrypted = load_note(filename)
                decrypted = decrypt_data(encrypted, note_password)
                try:
                    note_obj = json.loads(decrypted.decode())
                    content = note_obj.get("content", "")
                    tags = ", ".join(note_obj.get("tags", []))
                    self.print_output("Content: " + content + "\nTags: " + tags + "\n")
                except json.JSONDecodeError:
                    self.print_output("Content: " + decrypted.decode() + "\n")
            except Exception as e:
                self.print_output("Error: " + str(e) + "\n")
        elif command.startswith("edit"):
            filename = simpledialog.askstring("Edit Note", "Enter filename to edit:")
            if not filename: return
            note_password = simpledialog.askstring("Note Password", "Enter note password:", show="*")
            try:
                encrypted = load_note(filename)
                decrypted = decrypt_data(encrypted, note_password)
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
                new_encrypted = encrypt_data(new_note_json.encode(), note_password)
                filepath = os.path.join(NOTES_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(new_encrypted)
                self.print_output("Note updated.\n")
            except Exception as e:
                self.print_output("Error: " + str(e) + "\n")
        elif command.startswith("delete"):
            filename = simpledialog.askstring("Delete Note", "Enter filename to delete:")
            filepath = os.path.join(NOTES_DIR, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                self.print_output("Note deleted.\n")
            else:
                self.print_output("Note not found.\n")
        elif command.startswith("search"):
            search_term = simpledialog.askstring("Search", "Enter keyword to search:")
            note_password = simpledialog.askstring("Note Password", "Enter note password (assuming same for all notes):", show="*")
            found = False
            for f in os.listdir(NOTES_DIR):
                try:
                    encrypted = load_note(f)
                    decrypted = decrypt_data(encrypted, note_password)
                    try:
                        note_obj = json.loads(decrypted.decode())
                        content = note_obj.get("content", "").lower()
                        tags = " ".join(note_obj.get("tags", [])).lower()
                    except json.JSONDecodeError:
                        content = decrypted.decode().lower()
                        tags = ""
                    if search_term.lower() in content or search_term.lower() in tags:
                        self.print_output("Match found in: " + f + "\n")
                        found = True
                except Exception:
                    continue
            if not found:
                self.print_output("No matches found.\n")
        elif command.startswith("todo"):
            self.open_todo_menu()
        else:
            self.print_output("Unknown command.\n")
    
    def open_todo_menu(self):
        todo_win = tk.Toplevel(self)
        todo_win.title("Todo List")
        todo_win.geometry("400x300")
        listbox = tk.Listbox(todo_win)
        listbox.pack(fill=tk.BOTH, expand=True)
        # Load todos
        if os.path.exists(TODOS_FILE):
            try:
                with open(TODOS_FILE, "rb") as f:
                    encrypted_todos = f.read()
                todos_json = decrypt_data(encrypted_todos, self.master_password)
                todos = json.loads(todos_json.decode())
            except Exception as e:
                messagebox.showerror("Error", "Error loading todos: " + str(e))
                todos = []
        else:
            todos = []
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
                messagebox.showerror("Error", "Error saving todos: " + str(e))
        save_btn = tk.Button(todo_win, text="Save Todos", command=save_todos)
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)

# --- Improved GUI Version with Menu Bar ---
class ShadowNotesGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.master_password = verify_master_password()
        self.title("ShadowNotes GUI")
        self.geometry("900x600")
        self.create_menu()
        self.create_widgets()
        self.refresh_notes_list()
    
    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add Note", command=self.add_note)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "ShadowNotes v1.0"))
    
    def create_widgets(self):
        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.notes_listbox = tk.Listbox(left_frame, width=40)
        self.notes_listbox.pack(fill=tk.Y, expand=True)
        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(fill=tk.X)
        refresh_btn = tk.Button(btn_frame, text="Refresh List", command=self.refresh_notes_list)
        refresh_btn.pack(side=tk.LEFT, padx=2, pady=2)
        delete_btn = tk.Button(btn_frame, text="Delete Note", command=self.delete_note)
        delete_btn.pack(side=tk.LEFT, padx=2, pady=2)
        right_frame = tk.Frame(self)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.note_text = tk.Text(right_frame, wrap=tk.WORD)
        self.note_text.pack(fill=tk.BOTH, expand=True)
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        add_btn = tk.Button(bottom_frame, text="Add Note", command=self.add_note)
        add_btn.pack(side=tk.LEFT, padx=5)
        read_btn = tk.Button(bottom_frame, text="Read Note", command=self.read_note)
        read_btn.pack(side=tk.LEFT, padx=5)
        edit_btn = tk.Button(bottom_frame, text="Edit Note", command=self.edit_note)
        edit_btn.pack(side=tk.LEFT, padx=5)
        todo_btn = tk.Button(bottom_frame, text="Todo", command=self.open_todo_window)
        todo_btn.pack(side=tk.LEFT, padx=5)
    
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
        todo_win = tk.Toplevel(self)
        todo_win.title("Todo List")
        todo_win.geometry("400x300")
        listbox = tk.Listbox(todo_win)
        listbox.pack(fill=tk.BOTH, expand=True)
        # Load todos
        if os.path.exists(TODOS_FILE):
            try:
                with open(TODOS_FILE, "rb") as f:
                    encrypted_todos = f.read()
                todos_json = decrypt_data(encrypted_todos, self.master_password)
                todos = json.loads(todos_json.decode())
            except Exception as e:
                messagebox.showerror("Error", "Error loading todos: " + str(e))
                todos = []
        else:
            todos = []
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
                messagebox.showerror("Error", "Error saving todos: " + str(e))
        save_btn = tk.Button(todo_win, text="Save Todos", command=save_todos)
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)

# --- Launcher Window to choose between CLI and GUI ---
class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ShadowNotes Launcher")
        self.geometry("300x200")
        self.create_widgets()
    
    def create_widgets(self):
        label = tk.Label(self, text="Choose Interface", font=("Arial", 16))
        label.pack(pady=20)
        cli_button = tk.Button(self, text="CLI", width=15, command=self.launch_cli)
        cli_button.pack(pady=5)
        gui_button = tk.Button(self, text="GUI", width=15, command=self.launch_gui)
        gui_button.pack(pady=5)
    
    def launch_cli(self):
        master_password = verify_master_password()
        self.destroy()
        cli_window = tk.Tk()
        cli_window.title("ShadowNotes CLI")
        CLIFrame(cli_window, master_password)
        cli_window.mainloop()
    
    def launch_gui(self):
        master_password = verify_master_password()
        self.destroy()
        app = ShadowNotesGUI()
        app.mainloop()

if __name__ == "__main__":
    launcher = Launcher()
    launcher.mainloop()
