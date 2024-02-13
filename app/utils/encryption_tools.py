import json
import os
import base64
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Initialize environment variables
load_dotenv()

# Helper functions for encryption and decryption
def get_fernet():
    encryption_key_b64 = os.getenv('ENCRYPTION_KEY')
    if not encryption_key_b64:
        raise ValueError("ENCRYPTION_KEY is not set in environment variables")
    encryption_key = base64.urlsafe_b64decode(encryption_key_b64)
    return Fernet(encryption_key)

def encrypt_data(data):
    fernet = get_fernet()
    return fernet.encrypt(data.encode())

def decrypt_data(encrypted_data):
    fernet = get_fernet()
    return fernet.decrypt(encrypted_data).decode()

# JSON data handling
def load_json(filename):
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = decrypt_data(encrypted_data)
    return json.loads(decrypted_data)

def save_json(data, filename):
    encrypted_data = encrypt_data(json.dumps(data))
    with open(filename, 'wb') as file:
        file.write(encrypted_data)
