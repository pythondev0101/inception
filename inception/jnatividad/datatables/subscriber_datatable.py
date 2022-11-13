import pymongo
from bson import ObjectId
from flask import request
from flask.json import jsonify
from inception import MONGO
from inception.core.blueprints import bp_admin
from inception.jnatividad.models import Subscriber



@bp_admin.route('/subscribers/dt', methods=['GET'])
def fetch_subscribers_dt():
    draw = request.args.get('draw')
    start, length = int(request.args.get('start')), int(request.args.get('length'))
    search_value = request.args.get("search[value]")
    table_data = []
    
    role_id = MONGO.db.auth_user_roles.find_one({'name': 'Subscriber'})['_id']

    if search_value != '':
        
        query = list(MONGO.db.auth_users.aggregate([
            {"$match": {
                "role_id": ObjectId(role_id),
                "lname": {"$regex": search_value}
            }},
            {"$lookup": {"from": "bds_sub_areas", "localField": "sub_area_id",
                         "foreignField": "_id", 'as': "sub_area"}},
            {"$sort": {
                'lname': MONGO.ASCENDING
            }}
        ]))
        total_records = len(query)
    else:
        query = list(MONGO.db.auth_users.aggregate([
            {"$match": {"role_id": ObjectId(role_id)}},
            {"$lookup": {"from": "bds_sub_areas", "localField": "sub_area_id",
                         "foreignField": "_id", 'as': "sub_area"}},
            {"$sort": {
                'lname': pymongo.ASCENDING
            }},
            {"$skip": start},
            {"$limit": length},
        ]))
        total_records = len(Subscriber.find_all())

    filtered_records = len(query)

    for data in query:
        subscriber: Subscriber = Subscriber(data=data)
        table_data.append((
            str(subscriber.id),
            subscriber.lname,
            subscriber.fname,
            subscriber.sub_area.name if subscriber.sub_area is not None else '',
            subscriber.str_date_created,
            ''
        ))
        
    response = {
        'draw': draw,
        'recordsTotal': filtered_records,
        'recordsFiltered': total_records,
        'data': table_data
    }
    return jsonify(response)