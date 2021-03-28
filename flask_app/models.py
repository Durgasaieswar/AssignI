from datetime import datetime

from . import db


# CategoryMaster table
class CategoryMaster(db.Model):

    """category_master table in database

    Args:
        db (object): SQLAlchemy class object
    """

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(25), nullable=False)
    parent_cat = db.Column(db.String(25), nullable=False)
    event_master = db.relationship(
        'EventMaster',
        backref='category_master',
    )

    def __repr__(self):
        return f'<CategoryMaster {self.category}, {self.parent_cat}>'


# EventMaster table
class EventMaster(db.Model):

    """event_master table in database

    Args:
        db (object): SQLAlchemy class object
    """
    
    evnt_id = db.Column(db.Integer, primary_key=True)
    evnt_name = db.Column(db.String(30), nullable=False)
    place = db.Column(db.String(15), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    duration = db.Column(db.String(20), nullable=False)
    cast = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(25), nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('category_master.id'))

    def __repr__(self):
        return f'<EventMaster {self.evnt_id}, {self.evnt_name}, {self.place},' \
               f'{self.time}, {self.duration}, {self.cast}, {self.category}'
