import os 
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///safespace.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'safespace.kibo@gmail.com'
    MAIL_PASSWORD = 'FariEmmaGodFemi2023'

