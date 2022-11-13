from bson.objectid import ObjectId
from flask import (jsonify, request)
from flask_cors import cross_origin
from inception import MONGO
from inception.core.blueprints import bp_api
from inception.jnatividad.models import SubArea, Subscriber, Delivery



@bp_api.route('/api/sub-areas/<string:oid>/subscribers')
@cross_origin()
def get_sub_area_subscribers(oid):
    print("sub_area_id: ", oid)
    client_side = request.args.get('client_side', False)
    sub_area = SubArea.find_one_by_id(id=oid)

    if not sub_area:
        response = {
            'data': []
        }
        return jsonify(response)
    
    table_data = []

    if not client_side: # Serverside
        draw = request.args.get('draw')
        start, length = int(request.args.get('start')), int(request.args.get('length'))
        search_value = "%" + request.args.get("search[value]") + "%"
        column_order = request.args.get('column_order')
        billing_id = request.args.get('billing_id')

        if not sub_area:
            return jsonify({'data':[],'recordsTotal':0,'recordsFiltered':0,'draw':draw})

        role_id = MONGO.db.auth_user_roles.find_one({'name': 'Subscriber'})['_id']

        query = list(MONGO.db.auth_users.find({
            'role_id': ObjectId(role_id),
            'sub_area_id': sub_area.id
        }).skip(start).limit(length))

        total_records = len(list(MONGO.db.auth_users.find({
            'role_id': ObjectId(role_id),
            'sub_area_id': sub_area.id
        })))

        filtered_records = len(query)

        print("START: ", start)
        print("DRAW: ", draw)
        print("LENGTH: ", length)
        print("filtered_records: ", filtered_records)
        print("total_records: ", total_records)

        for data in query:
            subscriber = Subscriber(data=data)
            # delivery_query = Delivery.query.filter_by(
            #     billing_id=billing_id,subscriber_id=subscriber.id,active=1
            #     ).first()
            delivery: Delivery = Delivery(data=MONGO.db.bds_deliveries.find_one({
                'billing_id': ObjectId(billing_id),
                'subscriber_id': subscriber.id,
                'active': 1
            }))

            status = ""
            if delivery.status is not None and delivery.status != '':
                status = delivery.status
            else:
                status = "NOT YET DELIVERED"

            if column_order == "inline":
                table_data.append([
                    str(subscriber.id),
                    subscriber.contract_no,
                    subscriber.fname,
                    subscriber.lname,
                    subscriber.sub_area.name if subscriber.sub_area else ''
                ])
            else:
                table_data.append([
                    str(subscriber.id),
                    subscriber.contract_no,
                    subscriber.fname + " " + subscriber.lname,
                    subscriber.address,
                    status,
                    ""
                ])

        response = {
            'draw': draw,
            'recordsTotal': filtered_records,
            'recordsFiltered': total_records,
            'data': table_data
        }

        print(table_data)

        return jsonify(response)

    # Clientside
    for subscriber in sub_area.subscribers:
        table_data.append([
            subscriber.id,
            subscriber.contract_number,
            subscriber.fname,
            subscriber.lname,
            subscriber.sub_area.name if subscriber.sub_area else ''
        ])

    response = {
        'data': table_data
    }

    return jsonify(response)