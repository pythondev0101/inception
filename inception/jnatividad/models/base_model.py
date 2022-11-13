import pytz
from typing import Collection
from bson.objectid import ObjectId
from flask_login import current_user
from datetime import datetime

from inception import MONGO



TIMEZONE = pytz.timezone('Asia/Manila')


class BaseModel(object):
    _id: ObjectId
    active: bool
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str
    __collection__: Collection

    def __init__(self, data=None):
        self._id = ObjectId()
        
        if data is not None:
            self.__dict__.update(data)
            self._id = data.get('_id', None)
            self.active = data.get('active', True)
            self.created_at = data.get('created_at', None)
            self.updated_at = data.get('updated_at', None)
            self.created_by = data.get('created_by', None)
            self.updated_by = data.get('updated_by', None)
            return None

    def __repr__(self):
        return str(self.__dict__)

    @property
    def id(self):
        return self._id

    def save(self, session=None):
        self.created_at = datetime.utcnow()
        self.created_by = current_user.full_name if current_user is None else 'System'

        if session:
            self.__collection__.insert_one(self.__dict__, session=session)
        else:        
            self.__collection__.insert_one(self.__dict__)

    def update(self):
        pass
        # self.__collection__.update_one(
        #     {'_id': self._id},
        #     {'$set': self.__dict__})


    def delete(self):
        pass

    def toJson(self):
        json = self.__dict__
        
        for key,val in self.__dict__.items():
            json[key] = str(val)
        return json

    @classmethod
    def find_one_by_id(cls, id):
        try:
            query = cls.__collection__.find_one({'_id': ObjectId(id)})

            return cls(data=query)
        except Exception:
            return None

    @classmethod
    def count(cls):
        try:
            return cls.__collection__.find().count()
        except AttributeError:
            raise AttributeError("{model_name} Collection is not implemented".format(model_name=cls().__class__.__name__))

    @classmethod
    def find_all(cls):
        try:
            models = list(cls.__collection__.find().sort('created_at', MONGO.DESCENDING))
            
            data = []

            for model in models:
                data.append(cls(data=model))

            return data
        except AttributeError:
            raise AttributeError("{model_name} Collection is not implemented".format(model_name=cls().__class__.__name__))

    @classmethod
    def find_with_range(cls, start, length):
        try:
            models = list(cls.__collection__.find().sort('created_at', MONGO.DESCENDING).skip(start).limit(length))
            
            data = []

            for model in models:
                data.append(cls(data=model))

            return data
        except AttributeError:
            raise AttributeError("{model_name} Collection is not implemented".format(model_name=cls().__class__.__name__))

    @classmethod
    def search(cls, search):
        try:
            models = list(cls.__collection__.find(search).sort('created_at', MONGO.DESCENDING))
            
            data = []

            for model in models:
                data.append(cls(data=model))

            return data
        except AttributeError:
            raise AttributeError("{model_name} Collection is not implemented".format(model_name=cls().__class__.__name__))

    @property
    def created_at_local(self):
        local_datetime = ''
        if self.created_at is not None:
            local_datetime = self.created_at.replace(tzinfo=pytz.utc).astimezone(TIMEZONE)
            return local_datetime.strftime("%B %d, %Y %I:%M %p")
            
        return local_datetime

    @property
    def updated_at_local(self):
        local_datetime = ''
        if self.updated_at is not None:
            local_datetime = self.updated_at.replace(tzinfo=pytz.utc).astimezone(TIMEZONE)
            return local_datetime.strftime("%B %d, %Y %I:%M %p")
            
        return local_datetime
