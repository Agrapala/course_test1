import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # from env / k8s secret
    SQLALCHEMY_TRACK_MODIFICATIONS = False
