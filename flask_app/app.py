from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import jsonify, request

from .routes import CategoryListResource, CategoryPost, EventSingleResource, token_verify

from . import app, db, models, api

db.create_all()


@app.route('/login')
def login():
    """API to give JWT token for given user details with expiry time of
        10 minutes

    Returns:
        dict: JWT token | Message
    """

    auth = request.authorization
    if auth:
        token = jwt.encode(
            {
                'user': auth.username,
                'exp': datetime.utcnow() + timedelta(minutes=10)
            },
            app.config['SECRET_KEY']
        )
        return jsonify({'token': token.decode('UTF-8')})

    return jsonify({'token': "Please provide username & password,"
                             " to get the token"})


@app.route('/categories', methods=["GET"])
@token_verify
def get_categories():
    """API to show list of events by each category specific

    Returns:
        dict: Event details of each category
    """

    evnts = db.session.query(
        models.EventMaster.category,
        models.EventMaster.evnt_name,
        models.EventMaster.place,
        models.EventMaster.time
    ).join(
        models.CategoryMaster, models.CategoryMaster.id == models.EventMaster.cat_id
    ).order_by(models.EventMaster.category)
    # print(evnts)
    response = {}
    for evnt in evnts:
        print(evnt)
        if evnt[0] not in response.keys():
            response[evnt[0]] = []
        response[evnt[0]].append(
            {
                "Event_name": evnt[1],
                "Place": evnt[2],
                "Time": evnt[3]
            }
        )

    return jsonify(response)


@app.route('/top_three', methods=["GET"])
@token_verify
def top_three_get():
    """APT to show Top 3 Category based on number of events which
       associated with that category

    Returns:
        dict: Category names list
    """

    evnts = db.session.query(
        models.EventMaster.category
    ).join(
        models.CategoryMaster, models.CategoryMaster.id == models.EventMaster.cat_id
    ).group_by(models.EventMaster.category).order_by(
        db.func.count(models.EventMaster.category).desc()
    ).limit(3)
    # print(evnts)
    response = {"Category": []}
    for evnt in evnts:
        print(evnt)
        response["Category"].append(evnt[0])

    return jsonify(response)


@app.route('/delete_all/<cat_name>', methods=["DELETE"])
@token_verify
def delete_all(cat_name):
    """API to delete all data associated with given category name

    Args:
        cat_name (str): Name of category

    Returns:
        str: Message
    """

    models.EventMaster.query.filter_by(category=cat_name).delete()
    db.session.commit()
    return 'Successfully, given category details got deleted', 204


api.add_resource(CategoryPost, '/category')
api.add_resource(CategoryListResource, '/category/<int:page_number>/<int:page_limit>')
api.add_resource(EventSingleResource, '/category/<string:name>')

