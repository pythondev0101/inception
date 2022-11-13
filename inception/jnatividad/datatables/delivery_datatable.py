from flask_cors import cross_origin
import pymongo
from bson import ObjectId
from flask import request
from flask.json import jsonify
from inception import MONGO
from inception.core.blueprints import bp_admin
from inception.jnatividad.models import Delivery, Subscriber



@bp_admin.route('/billings/<string:billing_id>/sub-areas/<string:sub_area_id>/deliveries')
@cross_origin()
def get_billing_sub_area_deliveries(billing_id, sub_area_id):
    try:
        role_id = MONGO.db.auth_user_roles.find_one({'name': 'Subscriber'})['_id']

        query = list(MONGO.db.auth_users.find({
            'role_id': ObjectId(role_id),
            'sub_area_id': ObjectId(sub_area_id)
        }))

        table_data = []

        for data in query:
            subscriber: Subscriber = Subscriber(data=data)
            
            delivery_query = list(MONGO.db.bds_deliveries.aggregate([
                {'$match': {
                    'billing_id': ObjectId(billing_id),
                    'subscriber_id': ObjectId(subscriber.id),
                    'active': 1
                }},
                {'$lookup': {
                    'from': "auth_users", 
                    "localField": "subscriber_id", 
                    "foreignField": "_id",
                    'as': 'subscriber'
                    }},
                {'$lookup': {
                    'from': "bds_areas", 
                    "localField": "area_id", 
                    "foreignField": "_id",
                    'as': 'area'
                    }},
                {'$lookup': {
                    'from': "bds_sub_areas", 
                    "localField": "sub_area_id", 
                    "foreignField": "_id",
                    'as': 'sub_area'
                    }},
                {'$lookup': {
                    'from': "auth_users", 
                    "localField": "messenger_id", 
                    "foreignField": "_id",
                    'as': 'messenger'
                    }}
            ]))
            
            if len(delivery_query) > 0:
                delivery: Delivery = Delivery(data=delivery_query[0])
            else:
                delivery: Delivery = Delivery(data=None)
            
            status = ""
            if delivery.status is not None and delivery.status != '':
                status = delivery.status
            else:
                status = "NOT YET DELIVERED"
                
            table_data.append([
                str(subscriber.id),
                subscriber.contract_no,
                subscriber.fname + " " + subscriber.lname,
                subscriber.address,
                delivery.messenger.full_name if delivery.messenger is not None else '',
                delivery.date_mobile_delivery if status != "NOT YET DELIVERED" else '',
                delivery.remarks,
                status,
                "",
                delivery.image_path
            ])

        response = {
            'data': table_data
        }

        return jsonify(response), 200
    except Exception as err:
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500