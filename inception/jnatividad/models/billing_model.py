import pymongo
from datetime import datetime
from typing import Collection
from inception import MONGO
from inception.core import MongoObject
from inception.jnatividad.models.base_model import BaseModel



class Billing(MongoObject):
    _collection: Collection = MONGO.db.bds_billings

    billing_no: int
    full_billing_no: str
    name: str
    description: str
    # deliveries = db.relationship('Delivery', cascade='all,delete', backref="billing")
    date_from: datetime
    date_to: datetime
    active: bool
    
    def __init__(self, data=None):
        super(Billing, self).__init__(data=data)
        
        if data is not None:
            self.billing_no = data.get('billing_no', None)
            self.full_billing_no = data.get('full_billing_no', '')
            self.name = data.get('name', '')
            self.description = data.get('description', '')
            self.date_from = data.get('date_from', '')
            self.date_to = data.get('date_to', '')
            self.active = data.get('active', '')
            

    @classmethod
    def find_all(cls):
        try:
            models = list(cls._collection.find().sort('created_at', pymongo.DESCENDING))
            
            data = []

            for model in models:
                data.append(cls(data=model))

            return data
        except AttributeError:
            raise AttributeError("Collection is not implemented".format(model_name=cls().__class__.__name__))

