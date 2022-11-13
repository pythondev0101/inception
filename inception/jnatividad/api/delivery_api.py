import os
from datetime import datetime
from math import pi, cos, sqrt
from bson.objectid import ObjectId
from flask_cors.decorator import cross_origin
from werkzeug.utils import secure_filename
from flask import (jsonify, request, current_app)
from inception import CSRF, MONGO, S3
from inception.core.blueprints import bp_api
from inception.jnatividad.models import Billing, Delivery, Messenger, Subscriber, Area, SubArea



@bp_api.route('/confirm-deliver', methods=['POST'])
@CSRF.exempt
def confirm_deliver():
    longitude = request.form['longitude']
    latitude = request.form['latitude']
    accuracy = request.form['accuracy']
    messenger_id = request.form['messenger_id']
    subscriber_id = request.form['subscriber_id']
    date_mobile_delivery = request.form['date_mobile_delivery']
    remarks = request.form['remarks']

    try:
        active_billing = Billing(data=MONGO.db.bds_billings.find_one({
            'active': True
        }))
        
        deliveries_query = list(MONGO.db.bds_deliveries.aggregate([
            {'$match': {
                'subscriber_id': ObjectId(subscriber_id), 
                'active': 1,
                'status': "IN-PROGRESS",
                'billing_id': ObjectId(active_billing.id)
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
                }}
        ]))

        print(deliveries_query)
        delivery = Delivery(data=deliveries_query[0])

        print(date_mobile_delivery)

        date = datetime.strptime(str(date_mobile_delivery), '%Y-%m-%d %H:%M:%S')

        if delivery is None:
            return jsonify({'result': True})
        
        if delivery.subscriber.latitude is not None:
            if _isCoordsNear(longitude, latitude, delivery.subscriber, .2):
                delivery.status = "DELIVERED"
                print("DELIVERED", delivery.id)
            else:
                delivery.status = "PENDING"
                print("PENDING", delivery.id)
        else:
            subscriber = Subscriber.find_one_by_id(id=subscriber_id)
            messenger = Messenger.find_one_by_id(id=messenger_id)

            subscriber.latitude = latitude
            subscriber.longitude = longitude
            subscriber.accuracy = accuracy
            subscriber.updated_by = messenger.fname + " " + messenger.lname
            subscriber.updated_at = datetime.now()

            delivery.status = "DELIVERED"
            print("DELIVERED", delivery.id)

        img_file = request.files['file']
        if img_file is None:
            print("Image file is none!")
            return jsonify({'result': False})

        bucket = S3.Bucket('likes-bucket')
        bucket.Object(img_file.filename).put(Body=img_file)
        object_url = "https://likes-bucket.s3.ap-southeast-1.amazonaws.com/{}".format(img_file.filename)
        print("IMAGE SAVED", object_url)
        # filename = secure_filename(img_file.filename)
        # _img_path = os.path.join(current_app.config['UPLOAD_IMAGES_FOLDER'], filename)
        # img_file.save(_img_path)
        # print("IMAGE SAVED", subscriber_id)
        
        delivery.image_path = object_url
        delivery.messenger_id = ObjectId(messenger_id)
        delivery.delivery_longitude = longitude
        delivery.delivery_latitude = latitude
        delivery.accuracy = accuracy
        delivery.date_mobile_delivery = date
        delivery.date_delivered = datetime.utcnow()
        delivery.remarks = remarks

        MONGO.db.bds_deliveries.update_one({
            '_id': delivery.id,
        }, {'$set': {
            'status': delivery.status,
            'image_path': delivery.image_path,
            'messenger_id': delivery.messenger_id,
            'delivery_latitude': delivery.delivery_latitude,
            'delivery_longitude': delivery.delivery_longitude,
            'accuracy': delivery.accuracy,
            'date_mobile_delivery': delivery.date_mobile_delivery,
            'date_delivered': delivery.date_delivered,
            'remarks': delivery.remarks
        }})

        print("Database updated", delivery.id)

        return jsonify({
            'status': 'success',
            'data': {
                'id': str(delivery.id),
                'status': delivery.status,
                'image_path': delivery.image_path,
                }
            }), 200
    except Exception as err:
        print(err)
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500


@bp_api.route('/deliveries', methods=['GET'])
@cross_origin()
def get_deliveries():
    query_by = request.args.get('query')
    deliveries_query = []
    
    try:
        active_billing = Billing(data=MONGO.db.bds_billings.find_one({'active': True}))
        if active_billing is None:
            return jsonify({'deliveries': []})

        if not query_by == 'by_messenger':
            deliveries_query = list(MONGO.db.bds_deliveries.find({'active': 1}))
        else:
            messenger_id = request.args.get('messenger_id')
            messenger: Messenger = Messenger.find_one_by_id(id=messenger_id)

            deliveries_query = list(MONGO.db.bds_deliveries.aggregate([
                {'$match': {'area_id': {"$in": messenger.areas}, 'active': 1, 'billing_id': ObjectId(active_billing.id)}},
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
                    }}
            ]))

        table_data = []
        
        for data in deliveries_query:
            delivery: Delivery = Delivery(data=data)
            table_data.append({
                'id': str(delivery.id),
                'subscriber_id': str(delivery.subscriber_id),
                'subscriber_fname': delivery.subscriber.fname,
                'subscriber_lname': delivery.subscriber.lname,
                'subscriber_address': delivery.subscriber.address,
                'subscriber_email': delivery.subscriber.email,
                'delivery_date': delivery.delivery_date,
                'status': delivery.status,
                'longitude': delivery.subscriber.longitude,
                'latitude': delivery.subscriber.latitude,
                'area_id': str(delivery.area.id),
                'area_name': delivery.area.name,
                'sub_area_id': str(delivery.sub_area.id),
                'sub_area_name': delivery.sub_area.name,
                'image_path': delivery.image_path,
                'contract_no': delivery.subscriber.contract_no,
                'remarks': delivery.remarks
            })
        
        response = {
            'status': 'success',
            'data': table_data,
            'message': ''
        }
        return jsonify(response), 200
    except Exception as err:
        print(err)
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500


def _isCoordsNear(checkPointLng, checkPointLat, centerPoint: Subscriber, km):
    if checkPointLat is None or checkPointLng is None:
        return False
    
    if centerPoint.latitude in ["", None] or centerPoint.longitude in ["", None]:
        return False

    ky = 40000 / 360
    kx = cos(pi * float(centerPoint.latitude) / 180.0) * ky
    dx = abs(float(centerPoint.longitude) - float(checkPointLng)) * kx
    dy = abs(float(centerPoint.latitude) - float(checkPointLat)) * ky
    print("_isCoordsNear Result:", sqrt(dx * dx + dy * dy) <= km)
    return sqrt(dx * dx + dy * dy) <= km


def upload_file(file_name, bucket):
    # object_name = file_name
    # s3_client = boto3.client('s3')
    # response = s3_client.upload_file(file_name, bucket, object_name)
    # return response

    S3.Bucket('likes-bucket').upload_file()

