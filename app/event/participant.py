from flask import Blueprint, request, jsonify
from config.database import db
from app.models import Participant, Event,Organizer
from app.schema import participant_schema, participants_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

participant_bp = Blueprint('participant', __name__)

# Get all participants for a specific event (only if the logged-in user created the event)
@participant_bp.route('/event/<int:event_id>', methods=['GET'])
@jwt_required()
def get_event_participants(event_id):
    user_id = get_jwt_identity()
    event = Event.query.get_or_404(event_id)
    user = Organizer.query.get(user_id)

    if user.is_admin:
        participants = event.participants
        return jsonify(participants_schema.dump(participants))
    # Authorization check
    if int(event.organizer_id) != int(user_id):
        return jsonify({"message": "You do not have permission to view participants for this event"}), 403
    
    # Access participants through the relationship
    participants = event.participants
    return jsonify(participants_schema.dump(participants))

# Add a participant to a specific event (only if the logged-in user created the event)
@participant_bp.route('/event/<int:event_id>', methods=['POST'])
@jwt_required()
def create_event_participant(event_id):
    user_id = get_jwt_identity()
    event = Event.query.get_or_404(event_id)
    
    # Authorization check
    if int(event.organizer_id) != int(user_id):
        return jsonify({"message": "You do not have permission to add participants to this event"}), 403
    
    data = request.get_json()
    errors = participant_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    # Check if participant already exists by email (optional)
    participant = Participant.query.filter_by(email=data['email']).first()
    if not participant:
        participant = Participant(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            created_by=user_id
        )
        db.session.add(participant)
        db.session.commit()
    
    # Add the participant to the event if not already associated
    if participant not in event.participants:
        event.participants.append(participant)
        db.session.commit()
    
    return jsonify(participant_schema.dump(participant)), 201

@participant_bp.route('/<int:participant_id>', methods=['PUT'])
@jwt_required()
def update_participant(participant_id):
    user_id = get_jwt_identity()
    user = Organizer.query.get_or_404(user_id)
    participant = Participant.query.get_or_404(participant_id)

    # Check if the participant is associated with any event created by the logged-in user
    authorized = any(event.organizer_id == int(user_id) for event in participant.events)
    if not authorized and not user.is_admin:
        return jsonify({"message": "You do not have permission to update this participant"}), 403
    
    data = request.get_json()
    errors = participant_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    participant.name = data.get('name', participant.name)
    participant.email = data.get('email', participant.email)
    participant.phone = data.get('phone', participant.phone)
    
    db.session.commit()
    
    return jsonify({"message": "Participant updated successfully", "participant": participant_schema.dump(participant)})


# Get a specific participant only if the event organizer is the logged-in user
@participant_bp.route('/<int:participant_id>', methods=['GET'])
@jwt_required()
def get_participant(participant_id):
    user_id = get_jwt_identity()
    participant = Participant.query.get_or_404(participant_id)
    
    # Check if the participant is associated with an event created by the logged-in user
    authorized = any(event.organizer_id == int(user_id) for event in participant.events)
    if not authorized:
        return jsonify({"message": "You do not have permission to view this participant"}), 403
    
    return jsonify(participant_schema.dump(participant))

# Delete a participant only if the event organizer is the logged-in user
@participant_bp.route('/<int:participant_id>', methods=['DELETE'])
@jwt_required()
def delete_participant(participant_id):
    user_id = get_jwt_identity()
    user = Organizer.query.get_or_404(user_id)
    participant = Participant.query.get_or_404(participant_id)

    if user.is_admin:
        for event in participant.events:
            event.participants.remove(participant)
        db.session.delete(participant)
        db.session.commit()
        return jsonify({"message": "Participant deleted successfully (Admin)","participant":participant_schema.dump(participant)}), 200
    
    # Check if the participant is associated with any event created by the logged-in user
    authorized_events = [event for event in participant.events if int(event.organizer_id) == int(user_id)]
    if not authorized_events:
        return jsonify({"message": "You do not have permission to delete this participant"}), 403
    
    # Remove participant from all associated events first
    for event in authorized_events:
        event.participants.remove(participant)
    
    # Optionally delete the participant only if no other event is associated
    if not participant.events:
        db.session.delete(participant)
    
    db.session.commit()
    return jsonify({"message": "Participant deleted successfully","participant":participant_schema.dump(participant)})
