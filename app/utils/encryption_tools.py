import json
import os
import base64
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


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


def load_public_key(path_to_public_key):
    with open(path_to_public_key, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key


def load_private_key(path_to_private_key, password=None):
    with open(path_to_private_key, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=password.encode() if password else None,
            backend=default_backend()
        )
    return private_key



def encrypt_with_public_key(public_key, message):
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted


def decrypt_with_private_key(private_key, encrypted_message):
    original_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return original_message
