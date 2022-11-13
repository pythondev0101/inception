import pymongo
from flask import request
from flask.json import jsonify
from inception import MONGO
from inception.core.blueprints import bp_admin
from inception.jnatividad.models import SubArea



@bp_admin.route('/sub-areas/dt', methods=['GET'])
def fetch_sub_areas_dt():
    draw = request.args.get('draw')
    start, length = int(request.args.get('start')), int(request.args.get('length'))
    search_value = request.args.get("search[value]")
    table_data = []

    if search_value != '':
        query = SubArea.search(
            search={"name": {"$regex": search_value}},
        )
        total_records = len(query)
    else:
        query = list(MONGO.db.bds_sub_areas.aggregate([
            {"$lookup": {"from": "bds_areas", "localField": "area_id",
                         "foreignField": "_id", 'as': "area"}},
            {"$skip": start},
            {"$limit": length},
            {"$sort": {
                'created_at': pymongo.DESCENDING
            }}
        ]))
        total_records = len(SubArea.find_all())

    filtered_records = len(query)

    print("START: ", start)
    print("DRAW: ", draw)
    print("LENGTH: ", length)
    print("filtered_records: ", filtered_records)
    print("total_records: ", total_records)

    for data in query:
        sub_area: SubArea = SubArea(data=data)
        table_data.append((
            str(sub_area.id),
            sub_area.name,
            sub_area.description,
            sub_area.area.name if sub_area.area is not None else '',
            sub_area.str_date_created,
            ''
        ))
        
    response = {
        'draw': draw,
        'recordsTotal': filtered_records,
        'recordsFiltered': total_records,
        'data': table_data
    }
    return jsonify(response)
