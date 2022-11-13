from datetime import datetime
from bson.objectid import ObjectId
from flask import redirect, url_for, request, flash, jsonify
from flask.templating import render_template
from flask_cors.decorator import cross_origin
from flask_login import current_user, login_required
from inception import CSRF, MONGO
from inception.core.blueprints import bp_admin
from inception.jnatividad.models import SubArea, Subscriber, Delivery



@bp_admin.route('/subscribers')
@login_required
def subscribers():
    sub_areas = SubArea.find_all()
    return render_template("admin/jnatividad_subscriber_page.html", sub_areas=sub_areas)


@bp_admin.route('/subscribers/<string:subscriber_id>/billings')
@cross_origin()
def get_subscriber_billings(subscriber_id):
    # try:
    query = list(MONGO.db.bds_deliveries.aggregate([
        {'$match': {
            'subscriber_id': ObjectId(subscriber_id),
        }},
        {"$sort": {
            'created_at': MONGO.DESCENDING
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
            }},
    ]))
    
    table_data = []

    for data in query:
        billing: Delivery = Delivery(data=data)
        table_data.append([
            str(billing.subscriber_id),
            billing.status,
            billing.date_mobile_delivery if billing.messenger is not None else '',
            billing.messenger.full_name if billing.messenger is not None else '',
            "",
            billing.image_path
        ])

    response = {
        'data': table_data
    }

    return jsonify(response), 200
    # except Exception as err:
    #     return jsonify({
    #         'status': 'error',
    #         'message': str(err)
    #     }), 500


@bp_admin.route('/subscribers/create',methods=['POST'])
@login_required
def create_subscriber():
    form = request.form
 
    try:
        new = Subscriber()
        new.fname = form.get('fname', '')
        new.lname = form.get('lname', '')
        new.email = form.get('email', '')
        new.contract_no = form.get('contract_no', '')
        new.address = form.get('address', '')
        new.sub_area_id = ObjectId(form.get('sub_area')) if form.get('sub_area') != '' else None
        new.role_id = SUBSCRIBER_ROLE.id
        new.role_name = SUBSCRIBER_ROLE.name
        new.save()
        
        response = {
            'status': 'success',
            'data': new.toJson(),
            'message': "New subscriber added successfully!"
        }
        return jsonify(response), 201
    except Exception as err:
        print(err)
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500
           


@bp_admin.route('/subscribers/<string:oid>/edit',methods=['GET','POST'])
@login_required
def edit_subscriber(oid):
    ins = Subscriber.query.get_or_404(oid)
    form = SubscriberEditForm(obj=ins)

    if request.method == "GET":
        form.deliveries_inline.data = ins.deliveries

        return admin_edit(Subscriber, form, 'bp_bds.edit_subscriber', oid, 'bp_bds.subscribers', scripts=[{'bp_bds.static': 'js/subscriber.js'}],\
            extra_modal_template='bds/delivery/bds_details_modal.html')

    if not form.validate_on_submit():
        for key, value in form.errors.items():
            flash(str(key) + str(value), 'error')
        return redirect(url_for('bp_bds.subscribers'))

    try:
        ins.fname = form.fname.data
        ins.lname = form.lname.data
        ins.email = form.email.data if form.email.data != '' else None
        ins.address = form.address.data
        ins.sub_area_id = form.sub_area_id.data if form.sub_area_id.data != '' else None
        ins.longitude = form.longitude.data
        ins.latitude = form.latitude.data
        ins.contract_number = form.contract_number.data
        ins.updated_at = datetime.now()
        ins.updated_by = "{} {}".format(current_user.fname,current_user.lname)
        db.session.commit()
        flash('Subscriber update Successfully!','success')

    except Exception as e:
        flash(str(e),'error')
    return redirect(url_for('bp_bds.subscribers'))


@bp_admin.route('/api/subscriber/deliveries/<int:delivery_id>', methods=['GET'])
@CSRF.exempt
def get_subscriber_delivery(delivery_id):

    delivery = Delivery.query.get_or_404(delivery_id)
    print(delivery)
    if delivery is None:
        return jsonify({
            'id': False
        })

    accuracy = 0
    if delivery.accuracy:
        accuracy = round(float(delivery.accuracy), 2)

    # WE SERIALIZE AND RETURN LIST INSTEAD OF MODELS

    return jsonify({
        'id': delivery.id,
        'subscriber_id': delivery.subscriber.id,
        'subscriber_fname': delivery.subscriber.fname,
        'subscriber_lname': delivery.subscriber.lname,
        'subscriber_address': delivery.subscriber.address,
        'delivery_date': delivery.delivery_date,
        'status': delivery.status,
        'longitude': delivery.delivery_longitude,
        'latitude': delivery.delivery_latitude,
        'accuracy': accuracy,
        'date_mobile_delivery': delivery.date_mobile_delivery,
        'image_path': url_for('bp_bds.static', filename=delivery.image_path),
        'messenger_fname': delivery.messenger.fname,
        'messenger_lname': delivery.messenger.lname
    })