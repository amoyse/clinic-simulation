from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.encryption_tools import load_json, load_public_key, load_private_key, encrypt_with_public_key, decrypt_with_private_key
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


@medicloud.route('/api/get-data/<service>', methods=['GET'])
@jwt_required()
def get_data(service):

    # request_data = request.json
    # encrypted_request_b64 = request_data['encrypted_request']
    encrypted_request_b64 = service

    encrypted_request = base64.b64decode(encrypted_request_b64) 

    medicloud_private_key = load_private_key('app/services/medicloud/medicloud_private.pem', 'password')
    decrypted_request = decrypt_with_private_key(medicloud_private_key, encrypted_request)
    decrypted_request = decrypted_request.decode()
    
    # Load and filter data based on the decrypted request
    data = load_json('app/services/medicloud/simulated_database.json')
    service_data = data.get(decrypted_request, {})

    json_data = json.dumps(service_data)
    json_bytes = json_data.encode('utf-8')

    # Encrypt response data using FinCare's public RSA key (assumed to be securely exchanged beforehand)
    fincare_public_key = load_public_key('app/public_keys/fincare_public.pem')
    encrypted_response = encrypt_with_public_key(fincare_public_key, json_bytes)
    encrypted_response_b64 = base64.b64encode(encrypted_response).decode('utf-8')
    
    return encrypted_response_b64

