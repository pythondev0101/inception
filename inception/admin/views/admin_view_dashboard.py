from bson import ObjectId
from flask import jsonify, request
from inception import MONGO
from inception.core.blueprints import bp_admin
from inception.core import inception_render_template
from inception.jnatividad.models import Municipality, SubArea, Billing, Delivery, Area



@bp_admin.route('/dashboard')
def dashboard():
    municipalities = Municipality.find_all()
    return inception_render_template('admin/admin_dashboard.html', municipalities=municipalities)


@bp_admin.route('/dashboard/get-current-cycle-totals')
def get_current_cycle_totals():
    active_billing = MONGO.db.bds_billings.find_one({'active': True})
    if active_billing is None:
        raise Exception("Likes Error: No active billing")

    total_delivered = MONGO.db.bds_deliveries.find({
        'active': 1, 
        'billing_id': ObjectId(active_billing['_id']),
        'status': "DELIVERED"
    }).count()

    total_in_progress = MONGO.db.bds_deliveries.find({
        'active': 1, 
        'billing_id': ObjectId(active_billing['_id']),
        'status': "IN-PROGRESS"
    }).count()

    total_pending = MONGO.db.bds_deliveries.find({
        'active': 1, 
        'billing_id': ObjectId(active_billing['_id']),
        'status': "PENDING"
    }).count()
    
    response = {
        'status': "success",
        'data': {
            'total_delivered': total_delivered,
            'total_in_progress': total_in_progress,
            'total_pending': total_pending
        },
        "message": ""
    }
    
    print(response)
    return jsonify(response), 200

    


@bp_admin.route('/dashboard/get-delivery-summary')
def get_delivery_summary():
    municipality_id = request.args.get('municipality_id')
    areas = list(MONGO.db.bds_areas.find({'municipality_id': ObjectId(municipality_id)}))
    sub_areas = MONGO.db.bds_sub_areas.find({'area_id': {'$in': [ObjectId(area['_id']) for area in areas]}})
    sub_areas_names = [sub_area['name'] for sub_area in sub_areas]

    active_billing = MONGO.db.bds_billings.find_one({'active': True})
    if active_billing is None:
        raise Exception("Likes Error: No active billing")

    deliveries_query = list(MONGO.db.bds_deliveries.aggregate([
        {'$match': {
            'area_id': {'$in': [ObjectId(area['_id']) for area in areas]},
            'active': 1, 
            'billing_id': ObjectId(active_billing['_id'])
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
    
    datasets = [
        {
            'label': "Delivered",
            'data': [0 for _ in range(len(sub_areas_names))],
            'backgroundColor': 'rgb(75, 192, 192)'
        },
        {
            'label': "Pending",
            'data': [0 for _ in range(len(sub_areas_names))],
            'backgroundColor': 'rgb(255, 159, 64)'
        },
        {
            'label': "In-Progress",
            'data': [0 for _ in range(len(sub_areas_names))],
            'backgroundColor': 'rgb(255, 99, 132)'
        }
    ]

    for data in deliveries_query:
        delivery: Delivery = Delivery(data=data)
        try:
            sub_area_index = sub_areas_names.index(delivery.sub_area.name)
            if delivery.status == "DELIVERED":
                new_count = datasets[0]['data'][sub_area_index] + 1
                datasets[0]['data'][sub_area_index] = new_count
            elif delivery.status == "PENDING":
                new_count = datasets[1]['data'][sub_area_index] + 1
                datasets[1]['data'][sub_area_index] = new_count
            elif delivery.status == "IN-PROGRESS":
                new_count = datasets[2]['data'][sub_area_index] + 1
                datasets[2]['data'][sub_area_index] = new_count
                    
        except ValueError:
            continue

    response = {
        'status': "success",
        'data': {
            'labels': sub_areas_names,
            'datasets': datasets
        },
        "message": ""
    }
    return jsonify(response), 200
