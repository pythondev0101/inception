import pymongo
from inception import MONGO
from inception.auth.models.user_model import User
from inception.jnatividad.models import Area



class Messenger(User):
    _collection = MONGO.db.auth_users
    areas: list = []

    def __init__(self, data=None):
        super(Messenger, self).__init__(data=data)
        
        if data is not None:
            self.areas = data.get('areas', [])

    
    @property
    def areas_obj(self):
        areas = []
        for area_id in self.areas:
            areas.append(Area.find_one_by_id(id=area_id))
        return areas

    def update(self):
        self._collection.update_one({
            '_id': self.id
        },
        {'$set': {
            'fname': self.fname,
            'lname': self.lname,
            'email': self.email,
            'username': self.username,
            'areas': self.areas
            }
        })
        
        
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
