import os
from dotenv import load_dotenv



BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    load_dotenv()
    
    SECRET_KEY = os.environ.get('SECRET_KEY') # Key
    CORS_HEADERS = 'Content-Type' # Flask Cors


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    load_dotenv()
    
    MONGO_URI = os.environ.get('MONGO_URI_DEV')
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    load_dotenv()
    
    MONGO_URI = os.environ.get('MONGO_URI_PROD')
    DEBUG = False


APP_CONFIG = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
