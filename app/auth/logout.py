from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, unset_jwt_cookies, get_jwt_identity
from app.models import Organizer 
from app.schema import organizer_schema 

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    user_id = get_jwt_identity()
    user = Organizer.query.get_or_404(user_id)
    response = jsonify({"message": "Logout successful","user":organizer_schema.dump(user)})
    unset_jwt_cookies(response)
    return response