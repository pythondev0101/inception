from bson import ObjectId
from inception import MONGO
from inception.jnatividad.models.municipality_model import Municipality
from inception.jnatividad.models.base_model import BaseModel 
from inception.core import MongoObject



class Area(MongoObject):
    _collection = MONGO.db.bds_areas

    """ COLUMNS """
    name: str
    description: str
    municipality_id: ObjectId
    municipality: Municipality
    messengers: list
    
    def __init__(self, data=None):
        super(Area, self).__init__(data=data)
        
        if data is not None:
            self.name = data.get('name', '')
            self.description = data.get('description', '')
            self.municipality_id = data.get('municipality_id', '')

            if 'municipality' in data and len(data['municipality']) > 0:
                self.municipality = Municipality(data=data['municipality'][0])
            else:
                self.municipality = None

    @classmethod
    def find_all_by_municipality_id(cls, id):
        areas = list(cls._collection.aggregate([
            {"$match": {
                'municipality_id': ObjectId(id)
            }},
            {"$lookup": {"from": "bds_municipalities", "localField": "municipality_id",
                         "foreignField": "_id", 'as': "municipality"}}
        ]))

        data = []
        for area in areas:
            data.append(cls(data=area))
        return data

    @classmethod
    def find_one_by_name(cls, name):
        try:
            query = cls._collection.find_one({'name': name})
            return cls(data=query)
        except Exception:
            raise Exception("No area found from the name({}) given".format(name))
