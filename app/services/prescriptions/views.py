from flask import Blueprint, render_template, request, url_for, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.encryption_tools import load_public_key, load_private_key, encrypt_with_public_key, decrypt_with_private_key
from app.utils.decorators import role_required
from cryptography.fernet import Fernet
import requests
import base64


prescriptions = Blueprint('prescriptions', __name__)

@prescriptions.route('/')
@jwt_required()
@role_required(['doctor', 'nurse'])
def index():
    current_user = get_jwt_identity()
    if not current_user:
        return redirect(url_for('sso.check_auth'))
    data = get_content()
    return render_template("prescriptions.html", data=data)

def get_content():
    aes_key = Fernet.generate_key()

    data_to_send = "prescriptions".encode()
    
    # Encrypt the data with the AES key
    fernet = Fernet(aes_key)
    encrypted_data = fernet.encrypt(data_to_send)
    
    # Encrypt the AES key with Medicloud's public RSA key
    medicloud_public_key = load_public_key('app/public_keys/medicloud_public.pem')
    encrypted_aes_key = encrypt_with_public_key(medicloud_public_key, aes_key)
    
    encrypted_data_b64 = base64.b64encode(encrypted_data).decode('utf-8')
    encrypted_aes_key_b64 = base64.b64encode(encrypted_aes_key).decode('utf-8')
    
    payload = {
        'encrypted_data': encrypted_data_b64,
        'encrypted_aes_key': encrypted_aes_key_b64
    }

    # Send encrypted data and AES key to Medicloud
    response = requests.post('http://127.0.0.1:5000/medicloud/api/get-data', json=payload)
    
    if response.status_code == 200:
        encrypted_response_b64 = response.json()['encrypted_data']
        encrypted_response = base64.b64decode(encrypted_response_b64)
        
        decrypted_response = fernet.decrypt(encrypted_response).decode('utf-8')
        
        return decrypted_response
    else:
        return "Error: Unable to retrieve data from Medicloud"
