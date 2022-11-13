from bson.objectid import ObjectId
from flask import redirect, url_for, request, flash
from flask.json import jsonify
from flask.templating import render_template
from flask_login import login_required
from inception import MONGO
from inception.auth.models import User
from inception.core.blueprints import bp_admin
from inception.jnatividad.models import Messenger, Area



modals = [
    "bds/messenger/bds_add_area_modal.html"
]


@bp_admin.route('/messengers',methods=['GET'])
@login_required
def messengers():
    return render_template("admin/jnatividad_messenger_page.html")


@bp_admin.route('/messengers/<string:messenger_id>', methods=['GET'])
@login_required
def get_messenger(messenger_id):
    try:
        messenger = Messenger.find_one_by_id(id=messenger_id)
        
        areas = Area.find_all()
        
        messenger_areas = []
        available_areas = []
        
        area: Area
        for area in areas:
            if not area.id in messenger.areas:
                available_areas.append({
                    'id': str(area.id),
                    'name': area.name
                })
            else:
                messenger_areas.append({
                    'id': str(area.id),
                    'name': area.name
                })

        response = {
            'status': 'success',
            'data': {
                'id': str(messenger.id),
                'fname': messenger.fname,
                'lname': messenger.lname,
                'username': messenger.username,
                'email': messenger.email,
                'available_areas': available_areas,
                'messenger_areas': messenger_areas
            },
            'message': ""
        }
        return jsonify(response), 200
    except Exception as err:
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500



@bp_admin.route('/messengers/<string:messenger_id>')
@login_required
def get_messenger_details(messenger_id):
    try:
        messenger = User.find_one_by_id(id=messenger_id)

        response = {
            'status': 'success',
            'data': {
                'id': str(messenger.id),
                'fname': messenger.fname,
                'lname': messenger.lname,
                'username': messenger.username,
                'email': messenger.email,
            }
        }
        return jsonify(response), 200
    except Exception as err:
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 200


@bp_admin.route('/messengers/create', methods=["GET",'POST'])
@login_required
def create_messenger():
    if request.method == "GET":
        areas = Area.find_all()

        data = {
            'areas': areas,
        }

        return render_template(Messenger, "bds/messenger/bds_create_messenger.html", 'bds', title="Create messenger",\
            data=data, modals=modals)

    # try:
    new = Messenger()
    new.fname = request.form.get('fname', '')
    new.lname = request.form.get('lname', '')
    new.email = request.form.get('email', None)
    new.username = request.form.get('username', '')
    # new.role_id = MESSENGER_ROLE.id
    # new.role_name = MESSENGER_ROLE.name
    new.is_admin = 1 if request.form.get('is_admin') == 'on' else 0
    new.set_password("password")
    new.is_superuser = 0

    areas_line = request.form.getlist('areas[]')
    if areas_line:
        new.areas = [ObjectId(id) for id in areas_line]

    new.save()

    flash('New messenger added successfully!','success')
    # except Exception as exc:
    #     flash(str(exc), 'error')
    return redirect(url_for('admin.messengers'))


@bp_admin.route('/messengers/<string:oid>/edit',methods=['GET','POST'])
@login_required
def edit_messenger(oid):
    form = request.form
    print(form)
    selected_areas = form.getlist('selected_areas[]')
    print(selected_areas)

    new_areas = [ObjectId(area_id) for area_id in selected_areas]

    try:
        MONGO.db.auth_users.update_one({
            "_id": ObjectId(oid)
        }, {"$set": {
            "fname": form.get('fname'),
            'lname': form.get('lname'),
            'username': form.get('username'),
            'email': form.get('email'),
            'areas': new_areas
        }})
        
        response = {
            'status': 'success',
            'message': "Messenger updated Successfully!"
        }
        return jsonify(response), 201
    except Exception as err:
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500

    ins: Messenger = Messenger.find_one_by_id(id=oid)
    form = MessengerEditForm(obj=ins)

    print("ins.areas: ", ins.areas)
    if request.method == 'GET':
        areas_query = list(mongo.db.bds_areas.find({
            '_id': {'$nin': ins.areas}
        }))
        available_areas = [Area(data=data) for data in areas_query]
        data = {
            'areas': available_areas,
        }
        return admin_render_template(Messenger, 'bds/messenger/bds_edit_messenger.html', 'bds', oid=oid, ins=ins,form=form,\
            title="Edit Messenger", data=data, modals=modals)

    if not form.validate_on_submit():
        for key, value in form.errors.items():
            flash(str(key) + str(value), 'error')
        return redirect(url_for('admin.messengers'))

    # try:
    ins.fname = form.fname.data
    ins.lname = form.lname.data
    ins.email = form.email.data if form.email.data != '' else None
    ins.username = form.username.data

    areas_line = request.form.getlist('areas[]')
    ins.areas = []
    if areas_line:
        ins.areas = [ObjectId(id) for id in areas_line]
    ins.update()

    flash('Messenger update Successfully!','success')
    # except Exception as exc:
    #     flash(str(exc),'error')

    return redirect(url_for('bp_admin.messengers'))
