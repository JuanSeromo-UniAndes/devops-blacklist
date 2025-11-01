import json
import os
import boto3


def get_secret_value(secret_name, region='us-east-1'):
    """
    Get secret value from AWS Secrets Manager
    """
    secrets_client = boto3.client('secretsmanager', region_name=region)
    
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret'
    RDS_DB_NAME = os.environ.get('RDS_DB_NAME')
    RDS_USERNAME = os.environ.get('RDS_USERNAME')
    RDS_PASSWORD = os.environ.get('RDS_PASSWORD')
    secret_name = os.environ.get('RDS_HOSTNAME_SECRET', 'blacklist-rds-hostname')
    RDS_HOSTNAME = get_secret_value(secret_name)
    RDS_PORT = os.environ.get('RDS_PORT')
   
    if RDS_HOSTNAME:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_HOSTNAME}:{RDS_PORT}/{RDS_DB_NAME}?connect_timeout=10"
    else:
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@localhost:5432/blacklist_db?connect_timeout=10'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret'