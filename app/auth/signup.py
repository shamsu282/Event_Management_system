from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash
from config.database import db
from app.models import Organizer
from app.schema import organizer_schema

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if data['name'].strip()=="" or data['contact'].strip()=="" or data['organization'].strip()=="" or data['email'].strip()=="":
        return jsonify({"Message":"Field cannot be empty"})
    
    if len(data['contact'])>10 or len(data['contact'])<10:
        return jsonify({'Message':'Enter Proper Contact Number'})


    user= Organizer.query.filter_by(email=data['email']).first()

    if user:
        return jsonify({'message':'Email is already registered'})

    hashed_password = generate_password_hash(data['password']).decode('utf-8')  
    errors = organizer_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_user = Organizer(
        name=data['name'],
        contact = data['contact'],
        email = data['email'],
        organization=data['organization'],
        password =hashed_password,
        is_admin = (data.get("is_admin")=="True")
    )
    print(new_user)
    db.session.add(new_user)
    db.session.commit()
 
    return jsonify({"message": "User registered successfully", "user": organizer_schema.dump(new_user)}), 201
