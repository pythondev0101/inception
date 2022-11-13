from datetime import datetime
from decimal import Decimal
from bson import ObjectId
from inception import MONGO
from inception.jnatividad.models.base_model import BaseModel
from inception.jnatividad.models.subscriber_model import Subscriber
from inception.jnatividad.models.sub_area_model import SubArea
from inception.jnatividad.models.area_model import Area
from inception.jnatividad.models.messenger_model import Messenger



class Delivery(BaseModel):
    __collection__ = MONGO.db.bds_deliveries
    
    """ COLUMNS """
    billing_id: ObjectId= None
    subscriber_id: ObjectId = None
    _subscriber: Subscriber = None
    sub_area_id: ObjectId = None
    _sub_area: SubArea = None
    area_id: ObjectId = None
    _area: Area = None
    messenger_id: ObjectId = None
    _messenger: Messenger = None
    delivery_date: datetime = None
    date_delivered: datetime = None
    date_mobile_delivery: datetime = None
    status: str = None
    image_path: str = None
    accuracy: str = None
    delivery_longitude: Decimal = None
    delivery_latitude: Decimal = None
    remarks: str = "N/A"

    def __init__(self, data=None):
        super(Delivery, self).__init__(data=data)

        if data is not None:
            self.status = data.get('status')

            if 'subscriber' in data:
                self._subscriber = Subscriber(data=data['subscriber'][0])
            if 'area' in data:
                self._area = Area(data=data['area'][0])
            if 'sub_area' in data:
                self._sub_area = SubArea(data=data['sub_area'][0])
            if 'messenger' in data and len(data['messenger']) > 0:
                self._messenger = Messenger(data=data['messenger'][0])

    @property
    def subscriber(self):
        return self._subscriber

    @property
    def area(self):
        return self._area

    @property
    def sub_area(self):
        return self._sub_area

    @property
    def messenger(self):
        return self._messenger
