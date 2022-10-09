from bson import ObjectId
from pymongo.collection import Collection

from inception.core.event_repository import EventRepository



class MongoRepository(object):
    @staticmethod
    def retrieve(model: any, id: str):
        collection: Collection = model._collection
        return collection.find_one({'_id': ObjectId(id)})
    
    
    @staticmethod
    def update(model: any, data):
        collection: Collection = model._collection
        return collection.update_one({'_id': model._id}, data)
    
    
    @staticmethod
    def create(model: any, data):        
        collection: Collection = model._collection
        query = collection.insert_one(data)
        EventRepository.create(model)
        return query
    
    
    @staticmethod
    def find_one(model: any, filter):
        collection: Collection = model._collection
        return collection.find_one(filter)
    
    
    @staticmethod
    def find_many(model: any, filter):
        collection: Collection = model._collection
        return collection.find(filter)
    
    @staticmethod
    def count(model: any, filter):
        collection: Collection = model._collection
        return collection.find(filter).count()