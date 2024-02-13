from flask import Blueprint, render_template, request, url_for, redirect, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
from app.services.medicloud.views import get_data
from app.utils.encryption_tools import load_public_key, load_private_key, encrypt_with_public_key, decrypt_with_private_key
import base64

fincare = Blueprint('fincare', __name__)

@fincare.route('/')
@jwt_required()
def index():
    current_user = get_jwt_identity()
    if not current_user:
        return redirect(url_for('sso.check_auth'))
    data = get_content()
    return render_template("fincare.html", data=data)


def get_content():
    medicloud_public_key = load_public_key('app/public_keys/medicloud_public.pem')

    # Encrypt request data
    encrypted_request = encrypt_with_public_key(medicloud_public_key, "financial_transactions".encode())

    encrypted_request_b64 = base64.b64encode(encrypted_request).decode('utf-8')

    encrypted_response_b64 = get_data(encrypted_request_b64)


    # response = requests.post(
    #     "http://127.0.0.1:5000/medicloud/api/get-data",
    #     json={'encrypted_request': encrypted_request_b64}
    # )

    # Assuming the response contains encrypted data
    encrypted_response = base64.b64decode(encrypted_response_b64) 


    # Decrypt response data using FinCare's private RSA key
    fincare_private_key = load_private_key('app/services/fincare/fincare_private.pem', 'password')
    decrypted_data = decrypt_with_private_key(fincare_private_key, encrypted_response)

    return decrypted_data.decode('utf-8')
