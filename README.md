🔐 Password Manager (Terminal Version)
A secure and user-friendly terminal-based password manager built using Python and Tkinter. It includes features like password generation, strength analysis, encrypted vault storage, and a master password system.


✅ Features
🔑 Master Password Authentication

📊 Password Strength Analyzer

⚙️ Strong Password Generator

🔐 Encrypted Credential Vault

🖥️ Simple GUI using Tkinter

🔒 AES Encryption with Key Derivation (PBKDF2)

🚀 Getting Started
Prerequisites
Python 3.8 or above

Required Python packages (install using pip):

bash
Copy
Edit
pip install cryptography
Run the Application
bash
Copy
Edit
python pwdanalyze.py
On first run, you'll be prompted to set a master password. This password will be required every time you launch the app.

🔧 Functional Overview
1. Master Key Screen
Prompts user for the master password on startup.

2. Main Menu
Save Credentials
Store website, username, and password securely in the encrypted vault.

Generate / Analyze Password
Create strong passwords or test existing ones for complexity.

View Credentials
View stored credentials in a readable format (after authentication).

Exit
Securely close the app.

🔐 Security Details
Vault data is encrypted using AES (via Fernet from the cryptography library).

Master password is never stored directly; a derived key is verified using a salted hash.

Password vault and verification data are stored in:

vault.enc – Encrypted vault data

salt.bin – Used in key derivation

key.verifier – Stores encrypted verifier string

🧪 Example Use Case
Launch app via terminal
python pwdanalyze.py

Enter master password or create one on first run.

Choose to:

Generate and save new credentials

Analyze password strength

View saved credentials securely

📝 Notes
This app does not create a .exe file or standalone installer.

Meant to be run directly from the terminal using Python.

All credentials are stored locally and are encrypted.

Do not delete the salt.bin or key.verifier files or you will lose access.

💡 Future Enhancements
Auto-fill browser integration

Cloud sync with optional encryption key

Password breach check via APIs

CLI-only mode for headless use

🛡️ Disclaimer
This is a personal/educational project and not intended for enterprise-grade use. Use at your own risk.
