import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'alfamart_secret_key_2023'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///alfamart.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False