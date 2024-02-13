from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import load_json

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
    data = load_json('app/services/medicloud/simulated_database.json')
    if service is not None:
        data_name = ""
        if service == "fincare":
            data_name = "financial_transactions"
        elif service == "prescriptions":
            data_name = "prescriptions"
        elif service == "medrecords":
            data_name = "health_records"
        elif service == "careconnect":
            data_name = "health_records"

        service_data = data[data_name]
        if data_name != "":
            return jsonify({"success": True, "data": service_data})
        return jsonify({"success": False})

    # if not check_access(request.user, file_id):
    #     return jsonify({"success": False, "message": "Unauthorized"}), 403


