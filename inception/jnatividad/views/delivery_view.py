from re import sub
from bson.objectid import ObjectId
from flask.templating import render_template
from flask import (json, url_for, request,jsonify, abort)
from flask_login import login_required
from flask_cors import cross_origin
from inception import CSRF, MONGO, S3
from inception.core.blueprints import bp_admin
from inception.jnatividad.models import (
    Billing, Municipality, Subscriber, SubArea, Area, Messenger, Delivery
)



@bp_admin.route('/deliveries',methods=['GET'])
@login_required
def deliveries():
    billings = Billing.find_all()
    municipalities = Municipality.find_all()
    
    return render_template(
        'admin/jnatividad_delivery_page.html', 
        billings=billings,
        municipalities=municipalities
    )


@bp_admin.route('/subscribers/<string:subscriber_id>/delivery', methods=['GET'])
@cross_origin()
def get_delivery(subscriber_id):
    billing_id = request.args.get('billing_id')

    deliveries_query = list(MONGO.db.bds_deliveries.aggregate([
        {'$match': {
            'subscriber_id': ObjectId(subscriber_id), 
            'active': 1,
            'billing_id': ObjectId(billing_id)
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

    delivery = Delivery(data=deliveries_query[0])

    if delivery is None:
        return jsonify({
            'id': False
        })

    accuracy = 0
    if delivery.accuracy:
        accuracy = round(float(delivery.accuracy), 2)

    # WE SERIALIZE AND RETURN LIST INSTEAD OF MODELS

    print(delivery.image_path)
    return jsonify({
        'id': str(delivery.id),
        'subscriber_id': str(delivery.subscriber.id),
        'subscriber_fname': delivery.subscriber.fname,
        'subscriber_lname': delivery.subscriber.lname,
        'subscriber_address': delivery.subscriber.address,
        'delivery_date': delivery.delivery_date,
        'status': delivery.status,
        'longitude': delivery.delivery_longitude,
        'latitude': delivery.delivery_latitude,
        'accuracy': accuracy,
        'date_mobile_delivery': delivery.date_mobile_delivery,
        'image_path': delivery.image_path,
        'messenger_fname': delivery.messenger.fname,
        'messenger_lname': delivery.messenger.lname
    })


@bp_admin.route('/api/delivery/<string:delivery_id>/confirm', methods=['POST'])
@cross_origin()
def confirm_delivery_id(delivery_id):

    delivery = Delivery.find_one_by_id(id=delivery_id)

    if delivery is None:
        abort(404)

    delivery.status = "DELIVERED"

    MONGO.db.bds_deliveries.update_one({
        '_id': delivery.id,
    },{"$set":{
        'status': delivery.status
    }})

    return jsonify({
        'result':True, 
        'delivery': {'id': str(delivery.id),}
        })


@bp_admin.route('/api/subscribers/<string:subscriber_id>/deliveries/deliver', methods=['POST'])
@cross_origin()
def deliver(subscriber_id):
    billing_id = request.json['billing_id']

    subscriber = Subscriber.find_one_by_id(id=subscriber_id)
    sub_area = SubArea.find_one_by_id(id=subscriber.sub_area_id)
    delivery_query = MONGO.db.bds_deliveries.find_one({
        'billing_id': ObjectId(billing_id),
        'subscriber_id': subscriber.id,
        'active': 1
    })

    if not delivery_query:
        new_delivery: Delivery = Delivery()
        new_delivery.billing_id = ObjectId(billing_id)
        new_delivery.subscriber_id = subscriber.id
        new_delivery.sub_area_id = subscriber.sub_area_id
        new_delivery.area_id = ObjectId(sub_area.area_id)
        new_delivery.status = "IN-PROGRESS"
        new_delivery.active = 1
        new_delivery.save()

    response = jsonify({'result':True})

    return response


@bp_admin.route('/subscribers/<string:contract_no>/deliveries', methods=['POST'])
@CSRF.exempt
def deliver_subscriber_delivery(contract_no):
    # try:
        billing_id = request.json['billing_id']
        subscribers = Subscriber.find_all_by_contract_no(contract_no=contract_no)

        if subscribers is None:
            raise Exception("No subscriber found")

        if len(subscribers) > 1:
            raise Exception("Multiple subscriber with same the contract no.")

        subscriber: Subscriber = subscribers[0]

        sub_area: SubArea = SubArea.find_one_by_id(id=subscriber.sub_area_id)
        delivery_query = MONGO.db.bds_deliveries.find_one({
            'billing_id': ObjectId(billing_id),
            'subscriber_id': ObjectId(subscriber.id),
            'active': 1
        })

        response = {
            'status': 'success',
            'data': {},
            'message': ""
        }
        response['message'] = "Already scanned"

        if not delivery_query:
            new_delivery: Delivery = Delivery()
            new_delivery.billing_id = ObjectId(billing_id)
            new_delivery.subscriber_id = subscriber.get_object_id()
            new_delivery.sub_area_id = subscriber.sub_area_id
            new_delivery.area_id = ObjectId(sub_area.area_id)
            new_delivery.status = "IN-PROGRESS"
            new_delivery.active = 1
            new_delivery.save()
            response['message'] = "Success"
            response['data'] = [
                str(subscriber.id),
                subscriber.contract_no,
                subscriber.full_name,
                subscriber.address,
                '',
                '',
                "",
                new_delivery.status,
                ''
            ]
        return jsonify(response), 200
    # except Exception as err:
    #     print(err)
    #     return jsonify({
    #         'status': 'error',
    #         'message': str(err)
    #     }), 200


@bp_admin.route('/municipalities/<string:municipality_id>/areas', methods=['GET'])
@login_required
def get_municipality_areas(municipality_id):
    try:
        areas = Area.find_all_by_municipality_id(id=municipality_id)
        
        data = []
        
        area: Area
        for area in areas:
            data.append(area.toJson())

        response = {
            'status': 'success',
            'data': data,
            'message': ""
        }
        return jsonify(response), 200
    except Exception as err:
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 200


@bp_admin.route('/areas/<string:area_id>/sub-areas', methods=['GET'])
@login_required
def get_area_sub_areas(area_id):
    try:
        sub_areas = SubArea.find_all_by_area_id(id=area_id)
        
        data = []
        
        sub_area: SubArea
        for sub_area in sub_areas:
            data.append(sub_area.toJson())

        response = {
            'status': 'success',
            'data': data,
        }
        return jsonify(response), 200
    except Exception as err:
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 200


@bp_admin.route('/api/municipalities', methods=["GET"])
@cross_origin()
def get_municipalities():
    municipalities = Municipality.find_all()

    _data = []
    municipality: Municipality
    for municipality in municipalities:
        _data.append({
            'id': str(municipality.id),
            'name': municipality.name,
            'description': municipality.description
        })

    response = jsonify(_data)
    return response, 200


@bp_admin.route('/api/dtbl/billings', methods=['GET'])
@cross_origin()
def get_dtbl_billings():

    billings = Billing.find_all()

    _data = []

    billing: Billing
    for billing in billings:
        _data.append([
            str(billing.id),
            billing.active,
            billing.full_billing_no,
            billing.name,
            billing.date_from,
            billing.date_to,
        ])

    response = {
        'data': _data
        }

    print(response)

    return jsonify(response)


@bp_admin.route('/s3-upload', methods=['GET', 'POST'])
@CSRF.exempt
@cross_origin()
def s3_upload():
    if request.method == "GET":
        return render_template("bds/s3_upload.html")
    
    file = request.files['file']
    bucket = S3.Bucket('likes-bucket')
    bucket.Object(file.filename).put(Body=file)
    object_url = "https://likes-bucket.s3.ap-southeast-1.amazonaws.com/{}".format(file.filename)
    print(object_url)
    
    return "uploaded"
