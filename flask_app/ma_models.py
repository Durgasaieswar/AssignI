from .models import EventMaster

from . import ma


# Marshmallow schema
class EventMasterSchema(ma.Schema):

    """Marshmallow schema to serialize the SQLAlchemy data
    """

    class Meta:
        fields = ("evnt_id", "evnt_name", "cast", "time", "duration", "place", "category")
        model = EventMaster


evnt_schema = EventMasterSchema()
evnts_schema = EventMasterSchema(many=True)
