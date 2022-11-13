import os,sys
import certifi
import pymongo

from sensor.constant.database import DATABASE_NAME
from sensor.constant.env_variables import MONGODB_URL_KEY
from sensor.exception import SensorException
from sensor.logger import logging

ca = certifi.where()

class MongoDBClient:
    # client = None
    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            self.database_name = database_name
            # logging.info("started the Mongodb client connection")
            # if MongoDBClient.client is None:
            #     # mongo_db_url  = "mongodb+srv://<username>:<passowrd>@cluster0.n3qxk.mongodb.net/?retryWrites=true&w=majority"
            #     #first set env variable in Terminal by typing "SET MONGODB_URL_KEY" this command
            #     mongo_db_url = os.getenv(MONGODB_URL_KEY)
            #     if "localhost" in mongo_db_url:
            #         MongoDBClient.client = pymongo.MongoClient(mongo_db_url)
            #     else:
            #         MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            # self.client = MongoDBClient.client
            # self.database = self.client[database_name]
            # self.database_name = database_name
            # logging.info("completed the Mongodb client connection")
        except Exception as e:
            raise SensorException(e, sys)
    def mongo_client(self, ):
        try:
            logging.info("started the Mongodb client connection")
            client = None
            if client is None:
                # mongo_db_url  = "mongodb+srv://<username>:<passowrd>@cluster0.n3qxk.mongodb.net/?retryWrites=true&w=majority"
                #first set env variable in Terminal by typing "SET MONGODB_URL_KEY" this command
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if "localhost" in mongo_db_url:
                    client = pymongo.MongoClient(mongo_db_url)
                else:
                    client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            # client = MongoDBClient.client
            # database = MongoDBClient.client[self.database_name]
            # self.database_name = self.database_name
            logging.info("completed the Mongodb client connection")
            return client
        except Exception as e:
            logging.info(f"{e}")
            raise SensorException(e, sys)
