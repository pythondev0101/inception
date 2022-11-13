from datetime import datetime
from bson.objectid import ObjectId
from flask import (jsonify, request, abort)
from inception import CSRF, MONGO
from inception.core.blueprints import bp_api
from inception.jnatividad.models import Messenger, Subscriber



@bp_api.route('/subscriber/update-location',methods=["POST"])
@CSRF.exempt
def update_location():
    longitude = request.json['longitude']
    latitude = request.json['latitude']
    accuracy = request.json['accuracy']
    messenger_id = request.json['messenger_id']
    subscriber_id = request.json['subscriber_id']

    subscriber = Subscriber.find_one_by_id(id=subscriber_id)
    messenger = Messenger.find_one_by_id(id=messenger_id)

    subscriber.latitude = latitude
    subscriber.longitude = longitude
    subscriber.accuracy = accuracy
    subscriber.updated_by = messenger.fname + " " + messenger.lname

    MONGO.db.auth_users.update_one({
        '_id': subscriber.id
    }, {'$set': {
        'latitude': subscriber.latitude,
        'longitude': subscriber.longitude,
        'accuracy': subscriber.accuracy,
        'updated_by': subscriber.updated_by,
        'updated_at': datetime.utcnow()
    }})

    return jsonify({'result': True})


@bp_api.route('/api/subscribers/<string:subscriber_id>', methods=['GET'])
@CSRF.exempt
def get_subscriber(subscriber_id):
    query = list(MONGO.db.auth_users.aggregate([
        {"$match": {
            "_id": ObjectId(subscriber_id)
        }},
        {"$lookup": {"from": "bds_sub_areas", "localField": "sub_area_id",
                        "foreignField": "_id", 'as': "sub_area"}},
        {"$limit": 1}
    ]))
    
    if len(query) < 1:
        abort(404)

    # delivery = Delivery.query.filter_by(subscriber_id=subscriber.id,active=1).first()

    # _status = ""

    # if delivery:
    #     _status = delivery.status

    subscriber: Subscriber = Subscriber(data=query[0])

    data = {
        'id': str(subscriber.id),
        'fname': subscriber.fname,
        'lname': subscriber.lname,
        'address': subscriber.address,
        'latitude': subscriber.latitude,
        'longitude': subscriber.longitude,
        'email': subscriber.email,
        'status': "",
        'contract_no': subscriber.contract_no,
        'sub_area': subscriber.sub_area.name,
    }
    
    response = {
        'status': 'success',
        'data': data,
    }
    
    return jsonify(response)
