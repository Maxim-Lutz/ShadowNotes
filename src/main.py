import argparse
from encryption import encrypt_data, decrypt_data
from storage import save_note, load_note

def main():
    parser = argparse.ArgumentParser(description="ShadowNotes CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Befehl zum Hinzufügen einer Notiz
    add_parser = subparsers.add_parser("add", help="Add a new note")
    add_parser.add_argument("content", type=str, help="The content of the note (in Markdown)")
    
    # Befehl zum Lesen einer Notiz
    read_parser = subparsers.add_parser("read", help="Read a note")
    read_parser.add_argument("filename", type=str, help="Filename of the note to read")
    
    args = parser.parse_args()
    
    if args.command == "add":
        password = input("Enter password: ")
        data = args.content.encode()
        encrypted = encrypt_data(data, password)
        filename = save_note(encrypted)
        print(f"Note saved as {filename}")
    elif args.command == "read":
        password = input("Enter password: ")
        encrypted = load_note(args.filename)
        try:
            decrypted = decrypt_data(encrypted, password)
            print("Note content:")
            print(decrypted.decode())
        except ValueError as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
