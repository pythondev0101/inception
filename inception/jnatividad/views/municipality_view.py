from flask import request, flash, redirect, url_for
from flask.json import jsonify
from flask.templating import render_template
from flask_login import login_required
from inception.core.blueprints import bp_admin
from inception import MONGO
from inception.jnatividad.models import Municipality
from bson.objectid import ObjectId



@bp_admin.route('/municipalities')
@login_required
def municipalities():
    return render_template("admin/jnatividad_municipality_page.html")


@bp_admin.route('/municipalities/<string:municipality_id>', methods=['GET'])
@login_required
def get_municipality(municipality_id):
    try:
        muncipality = Municipality.find_one_by_id(id=municipality_id)

        response = {
            'status': 'success',
            'data': {
                'id': str(muncipality.id),
                'name': muncipality.name,
                'description': muncipality.description,
            },
            'message': ""
        }
        return jsonify(response), 200
    except Exception as err:
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500


@bp_admin.route('/municipalities/create', methods=['POST'])
@login_required
def create_municipality():
    form = request.form
 
    try:
        new = Municipality()
        new.name = form.get('name')
        new.description = form.get('description')
        MONGO.db.bds_municipalities.insert_one(new.toJson())
        flash("Successfully Saved!", 'success')
    except Exception as err:
        flash("Error Occured! Please try again", 'error')
    return redirect(url_for('admin.municipalities'))


@bp_admin.route('/municipalities/<string:oid>/edit', methods=['GET', 'POST'])
@login_required
def edit_municipality(oid):
    form = request.form
    
    try:
        MONGO.db.bds_municipalities.update_one({
            "_id": ObjectId(oid)
        }, {"$set": {
            "name": form.get('name'),
            'description': form.get('description'),
        }})
        
        response = {
            'status': 'success',
            'data': {},
            'message': "Municipality updated Successfully!"
        }
        return jsonify(response), 201
    except Exception as err:
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 200
