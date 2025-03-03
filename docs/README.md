
---

# **ShadowNotes**  

**ShadowNotes** is a simple, encrypted notes application focused on local storage security and minimalism.  

## **Features**  
- Encrypt and securely store notes  
- Command-line interface (CLI) for adding and reading notes  
- Notes are saved in an encrypted format  
- Built with Python using the `cryptography` library  

## **Installation**  

### **Requirements**  
- Python 3.x  
- `pip` (Python package manager)  

### **Setup**  
1. Clone the repository:  
   ```sh
   git clone https://github.com/maxim-lutz/ShadowNotes.git
   cd ShadowNotes
   ```
2. Create a virtual environment:  
   ```sh
   python -m venv venv
   ```
3. Activate the virtual environment:  
   - **Windows:**  
     ```sh
     venv\Scripts\activate
     ```
   - **Linux/macOS:**  
     ```sh
     source venv/bin/activate
     ```
4. Install dependencies:  
   ```sh
   pip install -r requirements.txt
   ```

## **Usage**  

### **Add a Note**  
```sh
python src/main.py add "Your secret note"
```
You will be prompted to enter a password to encrypt the note.  

### **Read a Note**  
```sh
python src/main.py read <filename>
```
You will need to enter the password used for encryption.  

## **Planned Features**  
- Graphical User Interface (GUI)  
- Synchronization options (self-hosted & cloud)  
- Mobile version  

## **License**  
ShadowNotes is open-source and released under the MIT License.  

---