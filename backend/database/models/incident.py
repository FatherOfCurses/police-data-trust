"""Define the SQL classes for Users."""
import enum


from ..core import CrudMixin, db

# Question: Should we be doing string enums?

class RecordType(enum.Enum):
    NEWS_REPORT = 1
    GOVERNMENT_RECORD = 2
    LEGAL_ACTION = 3
    PERSONAL_ACCOUNT = 4

class InitialEncounter(enum.Enum):
    UNKNOWN = 1
    TRAFFIC_VIOLATION = 2
    TRESSPASSING = 3
    POTENTIAL_CRIMINAL_SUSPECT = 4
    OTHER = 5


class VictimWeapon(enum.Enum):
    UNKNOWN = 1
    FIREARM = 2
    BLADE = 3
    BLUNT = 4
    NO_WEAPON = 5
    OTHER = 6


class VictimAction(enum.Enum):
    UNKNOWN = 1
    SPEAKING = 2
    NO_ACTION = 3
    FLEEING = 4
    APPROACHING = 5
    ATTACKING = 6
    OTHER = 7


class CauseOfDeath(enum.Enum):
    UNKNOWN = 1
    BLUNT_FORCE = 2
    GUNSHOT = 3
    CHOKE = 4
    OTHER = 5


class VictimStatus(enum.Enum):
    UNKNOWN = 1
    UNHARMED = 2
    INJURED = 3
    DISABLED = 4
    DECEASED = 5


# TODO: This file's a bit of a mess (my fault!)
#  There are a lot of association tables in here, and the incidents table is
#  not clearly either a facts table or component table.
#  We need to get a better idea of the relationships we want and then we should
#  implement them accordingly.


class Incident(db.Model, CrudMixin):
    """The incident table is the fact table."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_id = db.Column(db.Integer, db.ForeignKey("source.id"), nullable=False)
    source_details = db.relationship("SourceDetails", backref="incident", uselist=False)
    time_of_incident = db.Column(db.DateTime)
    complaint_date = db.Column(db.Date)
    closed_date = db.Column(db.Date)
    location = db.Column(db.Text)  # TODO: location object
    # Float is double precision (8 bytes) by default in Postgres
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    # TODO: neighborhood seems like a weird identifier that may not always
    #  apply in consistent ways across municipalities.
    neighborhood = db.Column(db.Text)
    description = db.Column(db.Text)
    stop_type = db.Column(db.Text)  # TODO: enum
    call_type = db.Column(db.Text)  # TODO: enum
    has_multimedia = db.Column(db.Boolean)
    from_report = db.Column(db.Boolean)
    # These may require an additional table. Also can dox a victim
    was_victim_arrested = db.Column(db.Boolean)
    arrest_id = db.Column(db.Integer)  # TODO: foreign key of some sort?
    # Does an existing warrant count here?
    criminal_case_brought = db.Column(db.Boolean)
    case_id = db.Column(db.Integer)  # TODO: foreign key of some sort?
    victims = db.relationship("Victim", backref="incident")
    suspects = db.relationship("Suspect", backref="incident")
    department = db.Column(db.Text)
    # descriptions = db.relationship("Description", backref="incident")
    tags = db.relationship("Tag", backref="incident")
    participants = db.relationship("Participant", backref="incident")
    attachments = db.relationship("Attachment", backref="incident")
    investigations = db.relationship("Investigation", backref="incident")
    results_of_stop = db.relationship("ResultOfStop", backref="incident")
    actions = db.relationship("Action", backref="incident")
    use_of_force = db.relationship("UseOfForce", backref="incident")
    legal_case = db.relationship("LegalCase", backref="incident")


class Description(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # description id
    incident_id = db.Column(
        db.Integer, db.ForeignKey("incident.id"), nullable=False
    )
    text = db.Column(db.Text)
    type = db.Column(db.Text)  # TODO: enum
    # TODO: are there rules for this column other than text?
    #source = db.Column(db.Text)
    # location = db.Column(db.Text)  # TODO: location object
    # # TODO: neighborhood seems like a weird identifier that may not always
    # #  apply in consistent ways across municipalities.
    # neighborhood = db.Column(db.Text)
    # stop_type = db.Column(db.Text)  # TODO: enum
    # call_type = db.Column(db.Text)  # TODO: enum
    # has_multimedia = db.Column(db.Boolean)
    # from_report = db.Column(db.Boolean)
    # # These may require an additional table. Also can dox a victim
    # was_victim_arrested = db.Column(db.Boolean)
    # arrest_id = db.Column(db.Integer)  # TODO: foreign key of some sort?
    # # Does an existing warrant count here?
    # criminal_case_brought = db.Column(db.Boolean)
    # case_id = db.Column(db.Integer)  # TODO: foreign key of some sort?


class SourceDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # source details id
    incident_id = db.Column(
        db.Integer, db.ForeignKey("incident.id"), nullable=False
    )
    record_type = db.Column(db.Enum(RecordType))
    # For Journalistic Publications
    publication_name = db.Column(db.Text)
    publication_date = db.Column(db.Date)
    publication_url = db.Column(db.Text)
    author = db.Column(db.Text)
    author_url = db.Column(db.Text)
    author_email = db.Column(db.Text)
    # For Government Records
    reporting_organization = db.Column(db.Text)
    reporting_organization_url = db.Column(db.Text)
    reporting_organization_email = db.Column(db.Text)
    # For Legal Records
    court = db.Column(db.Text)
    judge = db.Column(db.Text)
    docket_number = db.Column(db.Text)
    date_of_action = db.Column(db.Date)
