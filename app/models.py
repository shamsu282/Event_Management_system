from config.database import db
import datetime
import time

# Organizer Model
class Organizer(db.Model):
    __tablename__ = 'organizer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    organization = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationship to Event with a proper foreign key reference
    events = db.relationship('Event', backref='organizer', lazy='dynamic')

# Event Model
class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    
    organizer_id = db.Column(db.Integer, db.ForeignKey('organizer.id'), nullable=False)  

    # Many-to-many relationship with Participant using an association table
    participants = db.relationship('Participant', secondary='event_participant', backref='events', lazy=True)

# Association Table for Many-to-Many Relationship
event_participant = db.Table('event_participant',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('participant_id', db.Integer, db.ForeignKey('participant.id'), primary_key=True)
)

# Participant Model
class Participant(db.Model):
    __tablename__ = 'participant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)

    created_by = db.Column(db.Integer, db.ForeignKey('organizer.id'), nullable=False)  
