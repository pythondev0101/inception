import pymongo
from bson import ObjectId
from flask import request
from flask.json import jsonify
from inception import MONGO
from inception.core.blueprints import bp_admin
from inception.jnatividad.models import Billing



@bp_admin.route('/billings/dt', methods=['GET'])
def fetch_billings_dt():
    draw = request.args.get('draw')
    start, length = int(request.args.get('start')), int(request.args.get('length'))
    search_value = request.args.get("search[value]")
    table_data = []
    print("search_value", search_value)

    if search_value != '':
        query = Billing.search(
            search={"name": {"$regex": search_value}},
        )
        total_records = len(query)
    else:
        query = Billing.find_with_range(
            start=start,
            length=length
        )        
        total_records = len(Billing.find_all())

    filtered_records = len(query)

    print("START: ", start)
    print("DRAW: ", draw)
    print("LENGTH: ", length)
    print("filtered_records: ", filtered_records)
    print("total_records: ", total_records)

    billing: Billing
    for billing in query:
        table_data.append((
            str(billing.id),
            billing.full_billing_no,
            billing.description,
            billing.date_from,
            billing.date_to,
            billing.active,
            ''
        ))
        
    response = {
        'draw': draw,
        'recordsTotal': filtered_records,
        'recordsFiltered': total_records,
        'data': table_data
    }
    return jsonify(response)