import pymongo
from bson import ObjectId
from flask import request
from flask.json import jsonify
from inception import MONGO
from inception.core.blueprints import bp_admin
from inception.jnatividad.models import Messenger



@bp_admin.route('/messengers/dt', methods=['GET'])
def fetch_messengers_dt():
    draw = request.args.get('draw')
    start, length = int(request.args.get('start')), int(request.args.get('length'))
    search_value = request.args.get("search[value]")
    table_data = []

    if search_value != '':
        query = Messenger.search(
            search={"name": {"$regex": search_value}},
        )
        total_records = len(query)
    else:
        role_id = MONGO.db.auth_user_roles.find_one({'name': 'Messenger'})['_id']
        query = list(MONGO.db.auth_users.aggregate([
            {"$match": {"role_id": ObjectId(role_id)}},
            {"$lookup": {"from": "auth_user_roles", "localField": "role_id",
                         "foreignField": "_id", 'as': "role"}},
            {"$skip": start},
            {"$limit": length}
        ]))
        total_records = len(Messenger.find_all_by_role_id(ObjectId(role_id)))

    filtered_records = len(query)

    print("START: ", start)
    print("DRAW: ", draw)
    print("LENGTH: ", length)
    print("filtered_records: ", filtered_records)
    print("total_records: ", total_records)

    for data in query:
        messenger: Messenger = Messenger(data=data)
        
        table_data.append((
            str(messenger.id),
            messenger.username,
            messenger.fname,
            messenger.lname,
            messenger.email,
            ''
        ))
        
    response = {
        'draw': draw,
        'recordsTotal': filtered_records,
        'recordsFiltered': total_records,
        'data': table_data
    }
    return jsonify(response)

