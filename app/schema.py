from config.database import ma
from app.models import Organizer, Event, Participant


# Organizer Schema
class OrganizerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Organizer
        load_instance = True

# Event Schema
class EventSchema(ma.SQLAlchemyAutoSchema):
    organizer = ma.Nested(OrganizerSchema)  # Nested relationship

    class Meta:
        model = Event
        load_instance = True

# Participant Schema
class ParticipantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Participant
        load_instance = True

# Initialize schema instances
organizer_schema = OrganizerSchema()
organizers_schema = OrganizerSchema(many=True)
event_schema = EventSchema()
events_schema = EventSchema(many=True)
participant_schema = ParticipantSchema()
participants_schema = ParticipantSchema(many=True)
