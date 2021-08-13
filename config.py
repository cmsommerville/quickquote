

class BaseConfig():
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/qq-dev.db'


CONFIG = {
    "DEV": DevConfig
}
