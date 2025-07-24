import json
import os
from crypto_utils import encrypt_data, decrypt_data, load_master_password

VAULT_FILE = "vault.json"

def save_to_vault(website, username, password, key):
    if not os.path.exists(VAULT_FILE):
        data = []
    else:
        with open(VAULT_FILE, "rb") as file:
            encrypted = file.read()
            data = decrypt_data(encrypted, key) if encrypted else []

    data.append({
        "website": website,
        "username": username,
        "password": password
    })

    encrypted = encrypt_data(data, key)
    with open(VAULT_FILE, "wb") as file:
        file.write(encrypted)

def load_vault(key):
    if not os.path.exists(VAULT_FILE):
        return []
    with open(VAULT_FILE, "rb") as file:
        encrypted = file.read()
        if not encrypted:
            return []
        return decrypt_data(encrypted, key)

def search_credentials(website, key):
    records = load_vault(key)
    return [item for item in records if website.lower() in item['website'].lower()]

def delete_credential(website, key):
    records = load_vault(key)
    new_records = [item for item in records if item['website'].lower() != website.lower()]
    encrypted = encrypt_data(new_records, key)
    with open(VAULT_FILE, "wb") as file:
        file.write(encrypted)
    return len(records) != len(new_records)  # Return True if something was deleted
