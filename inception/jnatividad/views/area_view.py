from bson.objectid import ObjectId
from flask import request, render_template, jsonify
from flask_login import login_required
from inception import MONGO
from inception.core.blueprints import bp_admin
from inception.jnatividad.models import Municipality, Area



@bp_admin.route('/areas')
@login_required
def areas():
    municipalities = Municipality.find_all()
    return render_template("admin/jnatividad_area_page.html", municipalities=municipalities)


@bp_admin.route('/areas/<string:area_id>', methods=['GET'])
@login_required
def get_area(area_id):
    try:
        area = Area.find_one_by_id(id=area_id)

        response = {
            'status': 'success',
            'data': {
                'id': str(area.id),
                'name': area.name,
                'description': area.description,
                'municipality_id': str(area.municipality_id)
            },
            'message': ""
        }
        return jsonify(response), 200
    except Exception as err:
        print(err)
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500


@bp_admin.route('/areas/create', methods=["GET","POST"])
@login_required
def create_area():
    form = request.form
 
    try:
        new = Area()
        new.name = form.get('name', '')
        new.description = form.get('description', '')
        new.municipality_id = ObjectId(form.get('municipality')) if form.get('municipality') != '' else None
        new.save()

        response = {
            'status': 'success',
            'data': new.toJson(),
            'message': "New area added successfully!"
        }
        return jsonify(response), 201
    except Exception as err:
        print(err)
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500


@bp_admin.route('/areas/<string:oid>/edit', methods=['GET','POST'])
@login_required
def edit_area(oid):
    form = request.form
    
    try:
        MONGO.db.bds_areas.update_one({
            "_id": ObjectId(oid)
        }, {"$set": {
            "name": form.get('name'),
            'description': form.get('description'),
            'municipality_id': ObjectId(form.get('municipality')) if form.get('municipality') != '' else None
        }})
        
        response = {
            'status': 'success',
            'data': {},
            'message': "Area updated Successfully!"
        }
        return jsonify(response), 201
    except Exception as err:
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500
