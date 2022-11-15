import pymongo
from bson.objectid import ObjectId
from flask import request, flash, redirect, url_for, jsonify
from flask.templating import render_template
from flask_login import  login_required
from inception import MONGO
from inception.core.blueprints import bp_admin
from inception.jnatividad.functions import generate_number
from inception.jnatividad.models import Billing



@bp_admin.route('/billings')
@login_required
def billings():
    _billing_generated_number = ""

    # query = db.session.query(Billing).order_by(Billing.id.desc()).first()
    query_last_billing = list(MONGO.db.bds_billings.find().sort('created_at', pymongo.DESCENDING).limit(1))

    if query_last_billing:
        _billing_generated_number = generate_number("BILL", query_last_billing[0]['billing_no'])
    else:
        _billing_generated_number = "BILL00000001"

    return render_template("admin/jnatividad_billing_page.html", billing_generated_number=_billing_generated_number)


@bp_admin.route('/billings/new-generated-number', methods=['GET'])
def get_new_generated_number():
    try:
        generated_number = ""
        query_last_billing = list(MONGO.db.bds_billings.find().sort('created_at', pymongo.DESCENDING).limit(1))

        if query_last_billing:
            generated_number = generate_number("BILL", query_last_billing[0]['billing_no'])
        else:
            generated_number = "BILL00000001"

        response = {
            'status': 'success',
            'data': {
                'new_generated_number': generated_number
            },
            'message': ""
        }
        return jsonify(response), 200
    except Exception as err:
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 200


@bp_admin.route('/billings/<string:billing_id>', methods=['GET'])
@login_required
def get_billing(billing_id):
    try:
        billing = Billing.find_one_by_id(id=billing_id)

        response = {
            'status': 'success',
            'data': {
                'id': str(billing.id),
                'billing_no': billing.full_billing_no,
                'name': billing.name,
                'description': billing.description,
                'date_from': billing.date_from,
                'date_to': billing.date_to
            },
            'message': ""
        }
        return jsonify(response), 200
    except Exception as err:
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500


@bp_admin.route('/billings/create',methods=['POST'])
@login_required
def create_billing():
    form = request.form
    
    try:
        new = Billing()
        new.active = False
        new.full_billing_no = form.get('billing_no')
        new.description = form.get('description')
        new.date_to = form.get('date_to')
        new.date_from = form.get('date_from')
        new.billing_no = new.count() + 1
        new.save()
        flash("Successfully Saved!", 'success')
    except Exception as err:
        flash("Error Occured! Please try again", 'error')
    return redirect(url_for('admin.billings'))


@bp_admin.route('/billings/<string:oid>/edit',methods=['POST'])
@login_required
def edit_billing(oid):
    form = request.form
    print(oid)
    try:
        MONGO.db.bds_billings.update_one({
            "_id": ObjectId(oid)
        }, {"$set": {
            "name": form.get('name'),
            'description': form.get('description'),
            'date_from': form.get('date_from'),
            'date_to': form.get('date_to')
        }})
        
        response = {
            'status': 'success',
            'data': {},
            'message': "Billing updated Successfully!"
        }
        return jsonify(response), 201
    except Exception as err:
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500


@bp_admin.route('/billings/<string:billing_id>/set-active', methods=['POST'])
@login_required
def set_active(billing_id):
    status = request.json['status']
    try:
        with MONGO.cx.start_session() as session:
            with session.start_transaction():
                MONGO.db.bds_billings.update_many({
                    'active': True
                }, {"$set":{
                    'active': False
                }}, session=session)

                MONGO.db.bds_billings.update_one({
                    '_id': ObjectId(billing_id)
                },{"$set":{
                    'active': status
                }}, session=session)
        response = jsonify({
            'result': True
        })
        return response
    except Exception:
        return jsonify({'result': False})
