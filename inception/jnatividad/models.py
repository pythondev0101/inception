import pytz
from typing import Collection
from bson.objectid import ObjectId
from flask_login import current_user
import pymongo
from datetime import date, datetime
from decimal import Decimal

from inception import MONGO
from inception.auth.models.user_model import User
