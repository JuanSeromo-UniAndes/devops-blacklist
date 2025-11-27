import json
import os
import boto3


def get_secret_value(secret_name, region='us-east-1'):
    """
    Get secret value from AWS Secrets Manager
    """    
    try:
        secrets_client = boto3.client('secretsmanager', region_name=region)
        response = secrets_client.get_secret_value(SecretId=secret_name)
        raw_secret: str = response.get('SecretString', '')
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None
    
    # Attempt JSON unwrap
    if raw_secret.strip().startswith('{'):
        try:
            parsed = json.loads(raw_secret)
            if isinstance(parsed, dict) and len(parsed) == 1:
                # Return the single value (usual pattern for these secrets)
                return next(iter(parsed.values()))
            return parsed  # multi-key dict
        except json.JSONDecodeError:
            # Fall through to return original string
            pass
    return raw_secret

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret'
    RDS_DB_NAME = os.environ.get('RDS_DB_NAME')
    RDS_USERNAME = get_secret_value("blacklist-rds-username")
    RDS_PASSWORD = get_secret_value("blacklist-rds-password")
    RDS_HOSTNAME = get_secret_value('blacklist-rds-hostname')
    RDS_PORT = get_secret_value("blacklist-rds-port")

    print('hellodb', RDS_USERNAME, RDS_HOSTNAME)
   
    if RDS_HOSTNAME:
        print('hello host')
        SQLALCHEMY_DATABASE_URI = f"postgresql://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_HOSTNAME}:{RDS_PORT}/{RDS_DB_NAME}?connect_timeout=10"
    else:
        print('hello local', RDS_HOSTNAME)
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@blacklistdb.ci3w0yecas02.us-east-1.rds.amazonaws.com:5432/blacklistdb?connect_timeout=10'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret'