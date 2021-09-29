from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow

sess = Session()
db = SQLAlchemy()
mongo = PyMongo()
ma = Marshmallow()
