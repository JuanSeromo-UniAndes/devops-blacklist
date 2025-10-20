import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    RDS_HOSTNAME = os.environ.get('RDS_HOSTNAME') or "awseb-e-arkyanxh7q-stack-awsebrdsdatabase-nipmwcmbd2ag.ci3w0yecas02.us-east-1.rds.amazonaws.com"
    RDS_PORT = os.environ.get('RDS_PORT') or '5432'
    RDS_DB_NAME = os.environ.get('RDS_DB_NAME')
    RDS_USERNAME = os.environ.get('RDS_USERNAME')
    RDS_PASSWORD = os.environ.get('RDS_PASSWORD')

    if RDS_HOSTNAME:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_HOSTNAME}:{RDS_PORT}/{RDS_DB_NAME}"
    else:
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@localhost:5432/blacklist_db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret'