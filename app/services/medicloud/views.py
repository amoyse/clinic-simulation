from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.encryption_tools import load_json, load_public_key, load_private_key, encrypt_with_public_key, decrypt_with_private_key
from cryptography.fernet import Fernet
import base64
import json

medicloud = Blueprint('medicloud', __name__)

@medicloud.route('/')
@jwt_required()
def index():
    current_user = get_jwt_identity()
    if not current_user:
        return redirect(url_for('sso.check_auth'))
    return render_template("medicloud_upload.html")


@medicloud.route('/api/get-data', methods=['POST'])
def get_data():

    request_data = request.get_json()
    
    encrypted_aes_key_b64 = request_data.get('encrypted_aes_key')
    encrypted_data_b64 = request_data.get('encrypted_data')
    
    # Decode the Base64-encoded encrypted AES key and data
    encrypted_aes_key = base64.b64decode(encrypted_aes_key_b64)
    encrypted_data = base64.b64decode(encrypted_data_b64)
    
    # Decrypt the AES key using Medicloud's private RSA key
    medicloud_private_key = load_private_key('app/services/medicloud/medicloud_private.pem', 'password')
    aes_key = decrypt_with_private_key(medicloud_private_key, encrypted_aes_key)
    
    # Use the decrypted AES key to decrypt the data
    fernet = Fernet(aes_key)
    decrypted_data = fernet.decrypt(encrypted_data).decode('utf-8')
    
    data = load_json('app/services/medicloud/simulated_database.json')
    
    service_data = data.get(decrypted_data, {})
    
    encrypted_response_data = fernet.encrypt(json.dumps(service_data).encode('utf-8'))
    encrypted_response_data_b64 = base64.b64encode(encrypted_response_data).decode('utf-8')
    
    return jsonify({"encrypted_data": encrypted_response_data_b64})

