from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.database import db
from app.models import Organizer
from app.schema import organizer_schema, organizers_schema

organizer_bp = Blueprint('organizer', __name__)


@organizer_bp.route('/', methods=['GET'])
@jwt_required()
def get_organizers():
    organizers = Organizer.query.all()
    return jsonify(organizers_schema.dump(organizers))

@organizer_bp.route('/<int:organizer_id>', methods=['GET'])
@jwt_required()
def get_organizer(organizer_id):
    organizer = Organizer.query.get(organizer_id)
    if  not organizer:
        return  jsonify({'message':'No Organizer Found'})
    return jsonify(organizer_schema.dump(organizer))

@organizer_bp.route('/<int:organizer_id>', methods=['PUT'])
@jwt_required()
def update_organizer(organizer_id):
    user_id = get_jwt_identity()
    user = Organizer.query.get(user_id)
    organizer = Organizer.query.get_or_404(organizer_id)
    
    if user.is_admin != 'True':
        return jsonify({"message": "Only admins can update organizers"}), 403
    
    data = request.get_json()
    errors = organizer_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    organizer.name = data['name']
    organizer.contact = data['contact']
    organizer.organization = data['organization']
    db.session.commit()
    
    return jsonify(organizer_schema.dump(organizer))

@organizer_bp.route('/<int:organizer_id>', methods=['DELETE'])
@jwt_required()
def delete_organizer(organizer_id):
    user_id = get_jwt_identity()
    user = Organizer.query.get(user_id)
    organizer = Organizer.query.get_or_404(organizer_id)
    
    if not user.is_admin:
        return jsonify({"message": "Only admins can delete organizers"}), 403
    
    db.session.delete(organizer)
    db.session.commit()
    return jsonify({"message": "Organizer deleted successfully"})
