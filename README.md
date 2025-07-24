# 🔐 Password Manager 

A secure and interactive password manager built with Python and Tkinter.  
It includes password generation, strength analysis, encrypted vault storage, and master key protection — all within a clean terminal GUI interface.

---

## 📁 Project Structure

```
Password_Manager/
├── pwdanalyze.py           # Main GUI (Tkinter)
├── password_utils.py       # Password generation & strength analysis
├── crypto_utils.py         # Master password handling & encryption
├── vault_utils.py          # Credential vault logic
├── salt.bin                # Salt for key derivation
├── key.verifier            # Verifier for master password validation
└── vault.enc               # Encrypted credentials (auto-generated)
```

---

## ✅ Features

- 🔑 Master Password Protection  
- 🔐 AES-Encrypted Vault (Fernet)  
- 📊 Password Strength Analysis  
- 🔄 Strong Password Generator  
- 📁 Save & View Credentials  
- 🖥️ Clean GUI using Tkinter  

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.8+
- Required libraries:

```bash
pip install cryptography
```

---

### 🚀 Running the App

```bash
python pwdanalyze.py
```

- On **first launch**, you’ll be prompted to create a master password.
- On **subsequent launches**, you'll need to enter the master password to access the vault.

---

## 🧭 Functionality Overview

### 🔐 Master Key Entry  
Securely authenticates the user using a hashed and encrypted verifier.
  
### 🏠 Main Menu  
- **Save Credentials**  
  Input and store credentials (website, email/username, password) securely.

- **Generate / Analyze Password**  
  Create strong passwords and analyze the strength of existing ones.

- **View Saved Credentials**  
  Displays previously saved credentials in a readable, decrypted format.

- **Exit**  
  Securely closes the app.

---

## 🔒 Security Details

- Uses `cryptography.Fernet` (AES under the hood) for vault encryption.
- Master password is never stored — a derived key is used to validate identity via encrypted verifier.
- Key derivation is handled using PBKDF2HMAC with a unique salt.
- Files involved in securing your data:
  - `salt.bin` — Salt used to derive encryption key
  - `key.verifier` — Used to verify master password securely
  - `vault.enc` — Stores your encrypted credentials

---

## ⚠️ Important Notes

- ❌ No `.exe` or standalone executable — **runs directly via Python in terminal**.
- 💾 All data is stored **locally**, nothing is sent to the cloud.
- 🧨 If you delete `salt.bin` or `key.verifier`, you may **lose access permanently** to your stored credentials.

---

## 💡 Possible Future Additions

- 🔄 Cloud backup (encrypted)  
- 🌐 Browser integration  
- 🧪 Breach check with HaveIBeenPwned API  
- 📟 Full CLI-only version  

---

## 🛡️ Disclaimer

This project is built for educational and personal use.  
It is **not meant for enterprise-grade production environments**.  
Use at your own risk.

---
