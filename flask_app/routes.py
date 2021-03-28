from urllib.parse import unquote
import jwt
from functools import wraps
from datefinder import find_dates
from flask import request, jsonify
from flask_restful import Resource

from .ma_models import evnt_schema, evnts_schema
from .models import CategoryMaster, EventMaster

from . import db, app


def token_verify(func):
    """To verify token is from authorize user or not

    Args:
        func (function): API method

    Returns:
        dict: Response to be sent to user
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing!'})

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return jsonify({'message': 'Token is invalid or expired'})

        return func(*args, **kwargs)

    return decorated


# API's
class EventSingleResource(Resource):

    """category API with get, patch, delete methods

    """

    @token_verify
    def get(self, name):
        
        """ GET method of category API

        Args:
            name (str): Name of event

        Returns:
            dict: Details of given event
        """

        evnt = EventMaster.query.filter_by(evnt_name=name).first()
        return evnt_schema.dump(evnt)

    @token_verify
    def patch(self, name):

        """PATCH method of category API

        Args:
            name (str): Name of the event

        Returns:
            dict: updated details
        """

        evnt = EventMaster.query.filter_by(evnt_name=name).first()
        # payload = request.json
        if 'EventName' in request.json.keys():
            evnt.evnt_name = request.json["EventName"]
        if 'Place' in request.json.keys():
            evnt.place = request.json["Place"]
        if 'Time' in request.json.keys():
            evnt.time = request.json["Time"]
        if 'Duration' in request.json.keys():
            evnt.duration = request.json["Duration"]
        if 'Cast' in request.json.keys():
            evnt.cast = request.json["Cast"]
        if 'Category' in request.json.keys():
            evnt.category = request.json["Category"]
        if 'Parent' in request.json.keys():
            cm_evnt = CategoryMaster.query.filter_by(evnt_name=name).first()
            cm_evnt.parent_cat = request.json["Parent"]
        db.session.commit()
        return evnt_schema.dump(evnt)

    @token_verify
    def delete(self, name):

        """DELETE method of category API

        Args:
            name (str): Name of the event

        Returns:
            str: Message
        """

        name = unquote(name)
        evnt = EventMaster.query.filter_by(evnt_name=name).first()
        db.session.delete(evnt)
        db.session.commit()
        return 'Successfully, given details got deleted', 204


# API's
class CategoryListResource(Resource):

    @token_verify
    def get(self, page_number, page_limit):

        """GET method of category

        Args:
            page_number (int): Page number to view
            page_limit (int): Maximum rows to display in a page

        Returns:
            dict: event details
        """

        evnts_list = EventMaster.query.paginate(per_page=page_limit, page=page_number)
        # print(evnts_list)
        return evnts_schema.dump(evnts_list.items)


class CategoryPost(Resource):

    @token_verify
    def post(self):

        """POST method of category

        Returns:
            dict: category details
        """
        
        new_event = CategoryMaster(
            category=request.json["Category"],
            parent_cat=request.json["Parent"]
        )
        time_obj = list(find_dates(request.json["Time"]))[0]
        new_event.event_master.append(
            EventMaster(
                evnt_name=request.json["EventName"],
                place=request.json["Place"],
                time=time_obj,
                duration=request.json["Duration"],
                category=request.json["Category"],
                cast=request.json["Cast"]
            )
        )
        db.session.add(new_event)
        db.session.commit()
        return evnt_schema.dump(new_event)
