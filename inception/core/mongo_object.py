from datetime import datetime
from bson import ObjectId
import pymongo
from pymongo.collection import Collection
from inception.core.mongo_repository import MongoRepository



class MongoObject(object):
    _collection: Collection
    _filter: dict = {}

    _id: ObjectId
    date_created: datetime = None
    timezone = 'Asia/Manila'
    _code: str

    def __init__(self, data=None, **params):
        if data:
            self._id = data.get('_id', ObjectId())
            self.date_created = data.get('date_created')
            self._code = data.get('_code', None)
            
        if 'filter' in params:
            self._filter = params['filter']

    @property
    def id(self):
        if self._id is None:
            return None
        return str(self._id)


    @property
    def code(self):
        try:
            return self._code
        except AttributeError:
            raise NotImplementedError("Inception Error: 'code' must be implemented")


    @property
    def str_date_created(self):
        if self.date_created is None:
            return ''
        return str(self.date_created)
    
    
    def get_object_id(self):
        return self._id


    def __repr__(self):
        return str(self.__dict__)


    def count(self, filter=None):
        if filter is None:
            query = MongoRepository.count(self._filter)
        else:
            query = MongoRepository.count(filter)
        return query

    
    def update(self, fields_to_update=None):
        return MongoRepository.update(self)


    def create(self):
        self.date_created = datetime.utcnow()
        return MongoRepository.create(self, self.get_data())


    def get_data(self):
        self._code = self.get_code()
        return self.__dict__


    def get_code(self):
        return self.code


    @classmethod
    def retrieve(cls, id: str):
        query = MongoRepository


    @classmethod
    def find_one(cls, filter):
        query = MongoRepository.find_one(cls, filter)
        return cls(data=query)


    @classmethod
    def find_many(cls, filter, **params):
        query = MongoRepository.\
            find_many(cls, filter).\
                sort('date_created', pymongo.DESCENDING)
        
        if 'skip' in params:
            query.skip(params['skip'])
        
        if 'limit' in params:
            query.limit(params['limit'])
        
        if query is None:
            return []
        
        arr = []
        for x in query:
            arr.append(cls(data=x))
            
        return arr
