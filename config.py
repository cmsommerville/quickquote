import os
import urllib
from dotenv import load_dotenv

load_dotenv()

SQL_SERVER_CONNECTION_STRING = "Server={SERVER};Database={DB};UID={UID};PWD={PWD};"
SQL_SERVER_CONNECTION_STRING = "Driver={ODBC Driver 17 for SQL Server};" + SQL_SERVER_CONNECTION_STRING.format(**{
    "SERVER": os.getenv('DEV_DATABASE_SERVER'), 
    "DB": os.getenv('DEV_DATABASE_DB'), 
    "UID": os.getenv('DEV_DATABASE_UID'),
    "PWD": os.getenv('DEV_DATABASE_PWD')
})
params = urllib.parse.quote_plus(SQL_SERVER_CONNECTION_STRING)


class BaseConfig():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    PERMANENT_SESSION_LIFETIME = 3600


class DevConfig(BaseConfig):
    MONGO_URI = os.getenv("DEV_MONGO_URI")
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    SESSION_TYPE = os.getenv("SESSION_TYPE")
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"


class TestConfig(BaseConfig):
    MONGO_URI = os.getenv("DEV_MONGO_URI")
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_SQLALCHEMY_DATABASE_URI")
    SESSION_TYPE = os.getenv("SESSION_TYPE")
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"


CONFIG = {
    "DEV": DevConfig(),
    "TEST": TestConfig()
}
