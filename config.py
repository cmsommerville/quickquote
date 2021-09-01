import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    PERMANENT_SESSION_LIFETIME = 3600


class DevConfig(BaseConfig):
    MONGO_URI = os.getenv("DEV_MONGO_URI")
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_SQLALCHEMY_DATABASE_URI")
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
