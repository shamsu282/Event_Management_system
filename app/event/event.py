from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.database import db
from app.models import Event, Organizer
from app.schema import event_schema, events_schema

event_bp = Blueprint('event', __name__)

@event_bp.route('/', methods=['GET'])
@jwt_required(locations=["cookies"])
def get_events():
    user_id = get_jwt_identity()
    user = Organizer.query.get_or_404(user_id)

    if user.is_admin:
        events = Event.query.all()
        return jsonify(events_schema.dump(events))

    events = Event.query.filter_by(organizer_id=user_id).all()
    return jsonify(events_schema.dump(events))

@event_bp.route('/<int:event_id>', methods=['GET'])
@jwt_required(locations=["cookies"])
def get_event(event_id):
    user_id = get_jwt_identity()
    user = Organizer.query.get_or_404(user_id)
    
    if user.is_admin:
        event = Event.query.get_or_404(event_id)
        return jsonify(event_schema.dump(event))

    event = Event.query.get_or_404(event_id)
    if int(event.organizer_id) != int(user_id):
        return jsonify({"message": "You do not have permission to view this event"}), 403
    return jsonify(event_schema.dump(event))

@event_bp.route('/', methods=['POST'])
@jwt_required(locations=["cookies"])
def create_event():
    user_id = get_jwt_identity()
    user = Organizer.query.get(user_id)

    data = request.get_json()
    if data['name'].strip()=="" or data['description'].strip()=="" or data['date'].strip()=="" or data['location'].strip()=="":
        return jsonify({'Message':'Required all Fields'})
    
    existing_event = Event.query.filter_by(name=data['name'].strip(), organizer_id=user_id).first()
    if existing_event:
        return jsonify({'message': 'An event with this name already exists'}), 400
    
    errors = event_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    new_event = Event(
        name=data['name'],
        description=data['description'],
        date=data['date'],
        location=data['location'],
        organizer_id=user_id
    )
    db.session.add(new_event)
    db.session.commit()
    
    return jsonify(event_schema.dump(new_event)), 201

@event_bp.route('/<int:event_id>', methods=['PUT'])
@jwt_required(locations=["cookies"])
def update_event(event_id):
    user_id = get_jwt_identity()
    user = Organizer.query.get_or_404(user_id)
    event = Event.query.get_or_404(event_id)
    
    if not user.is_admin and int(event.organizer_id) != int(user_id):
        return jsonify({"message": "Only the event organizer or an admin can update this event"}), 403
    
    data = request.get_json()
    errors = event_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    event.name = data.get('name', event.name)
    event.description = data.get('description', event.description)
    event.date = data.get('date', event.date)
    event.location = data.get('location', event.location)
    
    db.session.commit()
    
    return jsonify({"message": "Event updated successfully"}, event_schema.dump(event))


@event_bp.route('/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    user_id = get_jwt_identity()
    user = Organizer.query.get_or_404(user_id)
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"message": " No Event found successfully"})

    if user.is_admin:
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Event deleted successfully"},event_schema.dump(event))

    
    if int(event.organizer_id) != int(user_id):
        return jsonify({"message": "Only the event organizer can delete this event"}), 403
    
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted successfully"},event_schema.dump(event))

