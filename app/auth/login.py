from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_csrf_token, set_access_cookies,JWTManager,set_refresh_cookies
from config.database import db
from app.models import Organizer
from app.schema import organizer_schema
from flask_bcrypt import check_password_hash

login_bp = Blueprint('login', __name__)



@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = Organizer.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=str(user.id))
        response = jsonify({"message": "Login successful", "user": organizer_schema.dump(user)})
        set_access_cookies(response, access_token)
        return response
    
    return jsonify({"message": "Invalid credentials"}), 401
