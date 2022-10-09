from typing import Collection
from inception import MONGO


_collection: Collection = MONGO.db.core_events

class EventRepository(object):
    @staticmethod
    def create(model: any):
        data = {
            'message': "A new {} was created".format(model.get_code()),
            'object_id': model.get_object_id(),
            'model': type(model).__name__,
            'type': 'created',
            'data': model.get_data()
        }
        
        return _collection.insert_one(data)
        