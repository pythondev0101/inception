import pymongo
from flask import request
from flask.json import jsonify
from inception import MONGO
from inception.core.blueprints import bp_admin
from inception.jnatividad.models import Area



@bp_admin.route('/areas/dt', methods=['GET'])
def fetch_areas_dt():
    draw = request.args.get('draw')
    start, length = int(request.args.get('start')), int(request.args.get('length'))
    search_value = request.args.get("search[value]")
    table_data = []

    if search_value != '':
        query = Area.search(
            search={"name": {"$regex": search_value}},
        )
        total_records = len(query)
    else:
        query = list(MONGO.db.bds_areas.aggregate([
            {"$lookup": {"from": "bds_municipalities", "localField": "municipality_id",
                         "foreignField": "_id", 'as': "municipality"}},
            {"$skip": start},
            {"$limit": length},
            {"$sort": {
                'created_at': pymongo.DESCENDING
            }}
        ]))
        total_records = len(Area.find_all())

    filtered_records = len(query)

    print("START: ", start)
    print("DRAW: ", draw)
    print("LENGTH: ", length)
    print("filtered_records: ", filtered_records)
    print("total_records: ", total_records)

    for data in query:
        area: Area = Area(data=data)
        table_data.append((
            str(area.id),
            area.name,
            area.description,
            area.municipality.name if area.municipality is not None else '',
            area.str_date_created,
            ''
        ))
        
    response = {
        'draw': draw,
        'recordsTotal': filtered_records,
        'recordsFiltered': total_records,
        'data': table_data
    }
    return jsonify(response)
