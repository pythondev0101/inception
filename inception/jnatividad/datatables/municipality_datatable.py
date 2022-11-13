from flask import request
from flask.json import jsonify
from inception.core.blueprints import bp_admin
from inception.jnatividad.models import Municipality



@bp_admin.route('/municipalities/dt', methods=['GET'])
def fetch_municipalities_dt():
    draw = request.args.get('draw')
    start, length = int(request.args.get('start')), int(request.args.get('length'))
    search_value = request.args.get("search[value]")
    table_data = []

    if search_value != '':
        query = Municipality.search(
            search={"name": {"$regex": search_value}},
        )
        total_records = len(query)
    else:
        query = Municipality.find_with_range(
            start=start,
            length=length
        )        
        total_records = len(Municipality.find_all())

    filtered_records = len(query)

    print("START: ", start)
    print("DRAW: ", draw)
    print("LENGTH: ", length)
    print("filtered_records: ", filtered_records)
    print("total_records: ", total_records)

    municipality: Municipality
    for municipality in query:
        table_data.append((
            str(municipality.id),
            municipality.name,
            municipality.description,
            municipality.str_date_created,
            ''
        ))
        
    response = {
        'draw': draw,
        'recordsTotal': filtered_records,
        'recordsFiltered': total_records,
        'data': table_data
    }
    return jsonify(response)