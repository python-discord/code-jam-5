import os

base_directory = os.path.abspath(os.path.dirname(__file__))



class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'testing123'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
