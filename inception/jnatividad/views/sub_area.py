from bson.objectid import ObjectId
from flask import request, jsonify, render_template
from flask_login import login_required
from inception import MONGO
from inception.core.blueprints import bp_admin
from inception.jnatividad.models import Area, SubArea, Subscriber



@bp_admin.route('/sub-areas')
@login_required
def sub_areas():
    areas = Area.find_all()
    return render_template("admin/jnatividad_sub_area_page.html", areas=areas)


@bp_admin.route('/sub-areas/<string:sub_area_id>', methods=['GET'])
@login_required
def get_sub_area(sub_area_id):
    try:
        sub_area = SubArea.find_one_by_id(id=sub_area_id)

        response = {
            'status': 'success',
            'data': {
                'id': str(sub_area.id),
                'name': sub_area.name,
                'description': sub_area.description,
                'area_id': str(sub_area.area_id)
            },
            'message': ""
        }
        return jsonify(response), 200
    except Exception as err:
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500


@bp_admin.route('/sub-areas/create', methods=['GET','POST'])
@login_required
def create_sub_area():
    form = request.form
 
    try:
        new = SubArea()
        new.name = form.get('name', '')
        new.description = form.get('description', '')
        new.area_id = ObjectId(form.get('area')) if form.get('area') != '' else None
        new.save()

        response = {
            'status': 'success',
            'data': new.toJson(),
            'message': "New sub area added successfully!"
        }
        return jsonify(response), 201
    except Exception as err:
        print(err)
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500    


@bp_admin.route('/sub-areas/<string:oid>/edit', methods=['GET','POST'])
@login_required
def edit_sub_area(oid):
    form = request.form
    
    try:
        MONGO.db.bds_sub_areas.update_one({
            "_id": ObjectId(oid)
        }, {"$set": {
            "name": form.get('name'),
            'description': form.get('description'),
            'area_id': ObjectId(form.get('area')) if form.get('area') != '' else None
        }})
        
        response = {
            'status': 'success',
            'data': {},
            'message': "Sub Area updated Successfully!"
        }
        return jsonify(response), 201
    except Exception as err:
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500


@bp_admin.route('/api/dtbl/subscribers')
def get_dtbl_subscribers():
    role_id = MONGO.db.auth_user_roles.find_one({'name': 'Subscriber'})['_id']
    
    query = list(MONGO.db.auth_users.aggregate([
        {"$match": {"role_id": ObjectId(role_id)}},
        {"$lookup": {"from": "auth_user_roles", "localField": "role_id",
                        "foreignField": "_id", 'as': "role"}},
        {"$lookup": {"from": "bds_sub_areas", "localField": "sub_area_id",
                        "foreignField": "_id", 'as': "sub_area"}}
    ]))

    table_data = []

    for data in query:
        subscriber: Subscriber = Subscriber(data=data)

        table_data.append([
            str(subscriber.id),
            subscriber.contract_no,
            subscriber.fname,
            subscriber.lname,
            subscriber.sub_area_name
        ])

    print("table_data: ", table_data)
    
    response = {
        'data': table_data
    }

    return jsonify(response)
