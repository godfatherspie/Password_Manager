import os
import sys
import base64
import json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Get the directory where the script or .exe is located
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)))

SALT_FILE = os.path.join(BASE_DIR, "salt.bin")
KEY_FILE = os.path.join(BASE_DIR, "key.verifier")

backend = default_backend()

def generate_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=backend
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

def setup_master_password(master_password: str):
    salt = os.urandom(16)
    key = generate_key(master_password, salt)

    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    with open(KEY_FILE, "wb") as f:
        f.write(key)

    return key

def load_master_password(master_password: str) -> bytes | None:
    if not os.path.exists(SALT_FILE) or not os.path.exists(KEY_FILE):
        return None

    with open(SALT_FILE, "rb") as f:
        salt = f.read()
    with open(KEY_FILE, "rb") as f:
        stored_key = f.read()

    try:
        derived_key = generate_key(master_password, salt)
        if derived_key == stored_key:
            return derived_key
        else:
            return None
    except Exception:
        return None

def encrypt_data(data: dict, key: bytes) -> bytes:
    f = Fernet(key)
    json_data = json.dumps(data).encode()
    return f.encrypt(json_data)

def decrypt_data(token: bytes, key: bytes) -> dict:
    f = Fernet(key)
    decrypted = f.decrypt(token)
    return json.loads(decrypted.decode())
