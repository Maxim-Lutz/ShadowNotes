import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import os
import json
from encryption import encrypt_data, decrypt_data
from storage import save_note, load_note, NOTES_DIR

class ShadowNotesGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ShadowNotes GUI")
        self.geometry("800x600")
        self.create_widgets()
        self.refresh_notes_list()

    def create_widgets(self):
        # Listbox to show notes on the left side
        self.notes_listbox = tk.Listbox(self, width=40)
        self.notes_listbox.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Frame for buttons next to the listbox
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
        
        # Text widget to display note content on the right side
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
        password = simpledialog.askstring("Password", "Enter password:", show="*")
        if password is None:
            return
        custom_filename = simpledialog.askstring("Custom Filename", "Enter custom filename (optional):")
        tags_input = simpledialog.askstring("Tags", "Enter tags (comma-separated, optional):")
        tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
        note_obj = {
            "content": note_content,
            "tags": tags
        }
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
        password = simpledialog.askstring("Password", "Enter password:", show="*")
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
        password = simpledialog.askstring("Password", "Enter password:", show="*")
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

if __name__ == "__main__":
    app = ShadowNotesGUI()
    app.mainloop()
