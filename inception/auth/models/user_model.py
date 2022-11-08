from flask_login import UserMixin
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from inception import MONGO, LOGIN_MANAGER
from inception.core import MongoRepository
from inception.core import MongoObject



class User(UserMixin, MongoObject):
    _collection = MONGO.db.auth_users
    
    username: str
    fname: str
    lname: str
    password_hash: str
    contact_no: str
    email_address: str
    role: str
    image_path: str = 'img/user_default_image.png'
    
    def __init__(self, data=None):
        MongoObject.__init__(self, data=data)
        
        if data:
            self.username = data.get('username', '')
            self.fname = data.get('fname', '')
            self.lname = data.get('lname', '')
            self.contact_no = data.get('contact_no', '')
            self.password_hash = data.get('password_hash', '')
            self.email_address = data.get('email_address', '')
            self.role = data.get('role', 'member')
            self.image_path = data.get('image_path', 'img/user_default_image.png')


    def set_password(self, password):
        self.password = password
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        return self.fname + " " + self.lname
        
        
    @classmethod
    def find_by_username(cls, username):
        query = MongoRepository.find_one(cls, {'username': username})
        if query is None:
            return None
        print(query)
        return cls(data=query)


    @property
    def code(self):
        self._code = "{}-{}".format(type(self).__name__, self.username) 
        return self._code

    
    @property
    def full_name(self):
        return self.fname + " " + self.lname


@LOGIN_MANAGER.user_loader
def load_user(user_id):
    print("user_id:::", user_id)
    user = User.find_one({'_id': ObjectId(user_id)})
    return user
