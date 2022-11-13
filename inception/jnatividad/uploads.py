import os, csv, platform
from bson.objectid import ObjectId
from flask import current_app, redirect, render_template, request, flash, url_for
from flask_login import login_required
from inception import MONGO
from inception.core.blueprints import bp_admin
from inception.jnatividad.models import Subscriber



@bp_admin.route('/upload/subscribers/csv', methods=['POST'])
@login_required
def upload_subscribers_csv():
    uploaded_file = request.files['csv_file']
    if uploaded_file.filename != '':
        file_path = os.path.join(current_app.config['UPLOAD_CSV_FOLDER'], uploaded_file.filename)
        
        if os.path.exists(file_path):
            flash("File exists!, (Rename the file then upload again)", 'error')
            return redirect(url_for('bp_bds.subscribers'))

        uploaded_file.save(file_path)

        role = MONGO.db.auth_user_roles.find_one({'name': 'Subscriber'})


        try:
            with open(file_path, encoding = "ISO-8859-1") as f:
                csv_file = csv.reader(f)
                with MONGO.cx.start_session() as session:
                    with session.start_transaction():
                        for _id,row in enumerate(csv_file):
                            if not _id == 0:
                                cycle = row[0]
                                type = row[1]
                                municipality = row[2]
                                area_name = row[3]
                                sub_area_name = row[4]
                                contract_no = row[5]
                                fname = row[6]
                                lname = row[7]
                                full_name = row[8]
                                full_address = row[9]

                                print(contract_no, fname,lname)
                                area = MONGO.db.bds_areas.find_one({'name': area_name}, session=session)
                                # area = Area.objects(name=area_name).first()
                                sub_area = MONGO.db.bds_sub_areas.find_one({'name': sub_area_name}, session=session)
                                # sub_area = SubArea.objects(name=sub_area_name).first()

                                new_area_id = ObjectId()

                                if area is None:
                                    MONGO.db.bds_areas.insert_one({
                                        '_id': new_area_id,
                                        'name': area_name,
                                        'description': ''
                                    },session=session)

                                new_sub_area_id = ObjectId()
                                if sub_area is None:
                                    
                                    sub_area_area_id = None
                                    if area is None:
                                        sub_area_area_id = new_area_id
                                    else:
                                        sub_area_area_id = area['_id']
                                    
                                    MONGO.db.bds_sub_areas.insert_one({
                                        '_id': new_sub_area_id,
                                        'name': sub_area_name,
                                        'description': '',
                                        'area_id': sub_area_area_id
                                    },session=session)

                                new = Subscriber()
                                new.contract_no = contract_no
                                new.fname = fname
                                new.lname = lname
                                new.address = full_address
                                new.establishment = type
                                new.cycle = cycle

                                if sub_area is None:
                                    new.sub_area_id = new_sub_area_id
                                else:
                                    new.sub_area_id = sub_area

                                MONGO.db.auth_users.insert_one({
                                    "_id": ObjectId(),
                                    "role_id": ObjectId(role['_id']),
                                    "role_name": role['name'],
                                    "contract_no": new.contract_no,
                                    "fname": new.fname,
                                    "lname": new.lname,
                                    "address": new.address,
                                    "establishment": new.establishment,
                                    "cycle": new.cycle,
                                    "sub_area_id": new_sub_area_id if sub_area is None else sub_area['_id'],
                                    "sub_area_name": sub_area_name if sub_area is None else sub_area['name']
                                },session=session)

                flash("Subscribers uploaded!", 'success')
    
        except Exception as exc:
            if os.path.exists(file_path):
                os.remove(file_path)

            flash(str(exc), 'error')
            
    return redirect(url_for('bp_bds.subscribers'))
