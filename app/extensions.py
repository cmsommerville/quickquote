from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow

sess = Session()
db = SQLAlchemy(engine_options={"fast_executemany": True})
# mongo = PyMongo()
ma = Marshmallow()
