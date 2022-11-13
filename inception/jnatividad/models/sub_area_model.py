from bson import ObjectId
from inception import MONGO
from bson import ObjectId
from inception import MONGO
from inception.jnatividad.models.base_model import BaseModel
from inception.jnatividad.models.area_model import Area
from inception.core import MongoObject


class SubArea(MongoObject):
    _collection = MONGO.db.bds_sub_areas

    """ COLUMNS """
    name: str
    description: str
    area_id: ObjectId
    area: Area

    def __init__(self, data=None):
        super(SubArea, self).__init__(data=data)
        
        if data is not None:
            self.name = data.get('name', '')
            self.description = data.get('description', '')
            self.area_id = data.get('area_id', '')

            if 'area' in data and len(data['area']) > 0:
                self.area = Area(data=data['area'][0])
            else:
                self.area = None


    @classmethod
    def find_all_by_area_id(cls, id):
        sub_areas = list(cls._collection.aggregate([
            {"$match": {
                "area_id": ObjectId(id)
            }},
            {"$lookup": {"from": "bds_areas", "localField": "area_id",
                         "foreignField": "_id", 'as': "area"}}
        ]))

        data = []
        for sub_area in sub_areas:
            data.append(cls(data=sub_area))
        return data

