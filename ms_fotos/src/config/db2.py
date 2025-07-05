import logging
import json
import base64
import boto3
from botocore.exceptions import ClientError
from sqlalchemy import create_engine, text
import sqlalchemy
from passlib.context import CryptContext

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Contexto para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

KEEPALIVE_KWARGS = {
    "keepalives": 1,
    "keepalives_idle": 30,
    "keepalives_interval": 5,
    "keepalives_count": 5,
}

class DB:
    _instance = None

    def __init__(self):
        if DB._instance is not None:
            raise ValueError("This class is a singleton, use DB.create()")
        else:
            DB._instance = self
        self.engine = self.create_engine()

    @staticmethod
    def create():
        if DB._instance is None:
            DB._instance = DB()
        return DB._instance
    
    @staticmethod
    def get_secret(secret_name):
        client = boto3.client('secretsmanager')

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            raise ValueError(f"Failed to retrieve secret '{secret_name}'") from e
        else:
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return json.loads(secret)

    def get_credentials(self):

        secret = DB.get_secret("Auth-Service-DB-ReservaT")
        return {
            'user': secret['user'],
            'password': secret['password'],
            'host': secret['host'],
            'port': secret['port'],
            'database': secret['database'],
        }

    def create_engine(self):
        credentials = self.get_credentials()
        
        try:
            engine = create_engine('{engine}://{user}:{password}@{host}:{port}/{database}'.format(
                engine='postgresql+psycopg2',
                user=credentials['user'],
                password=credentials['password'],
                host=credentials['host'],
                port=credentials['port'],
                database=credentials['database']
            ),
                pool_size=200,
                max_overflow=0,
                pool_recycle=60
            )
            return engine
            
        except Exception as e:
            logger.error(f"Error al conectar a la base de datos: {str(e)}")
            raise
            
meta = sqlalchemy.MetaData(schema="usr_app")