import os,sys
import certifi
import pymongo

from sensor.constant.database import DATABASE_NAME
from sensor.constant.env_variables import MONGODB_URL_KEY
from sensor.exception import SensorException

ca = certifi.where()

class MongoDBClient:
    client = None
    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                # mongo_db_url  = "mongodb+srv://<username>:<passowrd>@cluster0.n3qxk.mongodb.net/?retryWrites=true&w=majority"
                #first set env variable in Terminal by typing "SET MONGODB_URL_KEY" this command
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise SensorException(e, sys)
