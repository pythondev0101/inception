from datetime import datetime
from bson import ObjectId
import pymongo
from pymongo.collection import Collection
from flask_login import current_user
from inception import MONGO
from inception.core.mongo_repository import MongoRepository



class MongoObject(object):
    _collection: Collection
    _filter: dict = {}

    _id: ObjectId
    _data = {}
    date_created: datetime = None
    timezone = 'Asia/Manila'
    _code: str

    def __init__(self, data=None, **params):
        self._data = data
        
        if data:
            self.__dict__.update(data)
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


    def save(self, session=None):
        self.created_at = datetime.utcnow()
        self.created_by = current_user.full_name if current_user is None else 'System'

        if session:
            self._collection.insert_one(self.__dict__, session=session)
        else:        
            self._collection.insert_one(self.__dict__)

    
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
    
    
    @classmethod
    def find_all(cls):
        try:
            models = list(cls._collection.find().sort('created_at', pymongo.DESCENDING))
            data = []

            for model in models:
                data.append(cls(data=model))
            return data
        except AttributeError:
            raise AttributeError("{model_name} _collection is not implemented".format(model_name=cls().__class__.__name__))

    
    @classmethod
    def search(cls, filter):
        try:
            models = list(cls._collection.find(filter).sort('created_at', MONGO.DESCENDING))
            data = []

            for model in models:
                data.append(cls(data=model))
            return data
        except AttributeError:
            raise AttributeError("{model_name} _collection is not implemented".format(model_name=cls().__class__.__name__))


    @classmethod
    def find_with_range(cls, start, length):
        try:
            models = list(cls._collection.find().sort('created_at', pymongo.DESCENDING).skip(start).limit(length))
            data = []

            for model in models:
                data.append(cls(data=model))
            return data
        except AttributeError:
            raise AttributeError("{model_name} _collection is not implemented".format(model_name=cls().__class__.__name__))


    @classmethod
    def find_one_by_id(cls, id):
        try:
            query = cls._collection.find_one({'_id': ObjectId(id)})

            return cls(data=query)
        except Exception:
            return None


    def toJson(self):
        json = self.__dict__
        
        for key,val in self.__dict__.items():
            json[key] = str(val)
        return json
    
    