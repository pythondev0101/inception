from inception import MONGO
from inception.core import MongoObject



class Municipality(MongoObject):
    _collection = MONGO.db.bds_municipalities

    name: str
    description: str

    def __init__(self, data=None):
        super(Municipality, self).__init__(data=data)

        if data is not None:
            self.name = data.get('name', '')
            self.description = data.get('description', '')

    @classmethod
    def find_one_by_name(cls, name):
        try:
            query = cls._collection.find_one({'name': name})
            return cls(data=query)
        except Exception:
            raise Exception("No municipality found from the name({}) given".format(name))
