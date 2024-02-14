from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from dotenv import load_dotenv
from app.utils.encryption_tools import load_json, load_public_key, load_private_key, encrypt_with_public_key, decrypt_with_private_key, encrypt_data, decrypt_data
from app.utils.decorators import role_required
from cryptography.fernet import Fernet
from werkzeug.utils import secure_filename
import base64
import json
import os


load_dotenv()

medicloud = Blueprint('medicloud', __name__)

@medicloud.route('/')
@jwt_required()
@role_required(['researcher', 'admin'])
def index():
    current_user = get_jwt_identity()
    claims = get_jwt()
    user_role = claims.get('role')
    if not current_user:
        return redirect(url_for('sso.check_auth'))
    return render_template("medicloud_upload.html", uploaded=False, user_role=user_role)


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


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'docx', 'json'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@medicloud.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        data = file.read()
        encrypted_data = encrypt_data(data, True)

        with open(os.path.join('app/services/medicloud/uploads', filename), 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

        return render_template("medicloud_upload.html", uploaded=True, user_role='')
    return jsonify({'error': 'Invalid filetype'}), 400


