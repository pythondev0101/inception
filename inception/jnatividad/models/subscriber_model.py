from bson.objectid import ObjectId
from inception import MONGO
from inception.auth.models.user_model import User
from inception.jnatividad.models import SubArea



class Subscriber(User):
    __tablename__ = 'bds_subscribers'
    __amname__ = 'subscriber'
    __amdescription__ = 'Subscribers'
    __amicon__ = 'pe-7s-users'
    __view_url__ = 'bp_bds.subscribers'
    __collection__ = MONGO.db.auth_users

    """ COLUMNS """
    mname: str
    contract_no: str
    address: str
    mobile_no: str
    email: str
    longitude: str
    latitude: str
    accuracy: str
    cycle: int
    establishment: str
    # deliveries = db.relationship('Delivery', cascade='all,delete', backref="subscriber",order_by="desc(Delivery.delivery_date)")
    sub_area_id: ObjectId
    sub_area: SubArea
    sub_area_name: str

    def __init__(self, data=None):
        super(Subscriber, self).__init__(data=data)
        
        if data is not None:
            self.mname = data.get('mname', '')
            self.contract_no = data.get('contract_no', '')
            self.address = data.get('address', '')
            self.mobile_no = data.get('mobile_no')
            self.email = data.get('email', '')
            self.longitude = data.get('longitude', None)
            self.latitude = data.get('latitude', None)
            self.accuracy = data.get('accuracy', None)
            self.sub_area_name = data.get('sub_area_name', '')

            if 'sub_area' in data and len(data['sub_area']) > 0:
                self.sub_area = SubArea(data=data['sub_area'][0])
            else:
                self.sub_area = None

    @property
    def url(self):
        return "bp_bds.subscribers"


    @classmethod
    def find_all_by_contract_no(cls, contract_no, session=None):
        if session:
            query = list(cls._collection.aggregate([
                {"$match": {"contract_no": contract_no}},
                {"$lookup": {"from": "auth_user_roles", "localField": "role_id",
                            "foreignField": "_id", 'as': "role"}},
            ],session=session))
        else:
            query = list(cls._collection.aggregate([
                {"$match": {"contract_no": contract_no}},
                {"$lookup": {"from": "auth_user_roles", "localField": "role_id",
                            "foreignField": "_id", 'as': "role"}},
            ]))

        if len(query) <= 0:
            return None

        data = []
        for subscriber in query:
            data.append(cls(data=subscriber))
        return data
