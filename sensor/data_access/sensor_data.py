import sys
from typing import Optional

import numpy as np
import pandas as pd

from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.constant.database import DATABASE_NAME
from sensor.exception import SensorException
from sensor.logger import logging


class SensorData:
    """
    This class help to export entire mongo db record as pandas dataframe
    """

    def __init__(self):
        try:
            # conection to the mongodb client.
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)

        except Exception as e:
            raise SensorException(e, sys)

    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        This method id used to export entire collectin as dataframe:

        Args:
            collection_name (str): name of the collection of Mongodb
            database_name (Optional[str], optional): database name of mongodb. Defaults to None.

        Raises:
            SensorException: Error

        Returns:
            pd.DataFrame: pd.DataFrame of collection
        """
        try:
            logging.info("started the exporting collection as dataframe")
            if database_name is None:
                collection = self.mongo_client.database[collection_name]

            else:
                collection = self.mongo_client[database_name][collection_name]
            # Creating the Dataframe.
            df = pd.DataFrame(list(collection.find()))

            # If "_id" is there we are dropping that column.
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            # Replacing the na values with np.nan.
            df.replace({"na": np.nan}, inplace=True)
            logging.info("completed the exporting collection as dataframe")
            return df

        except Exception as e:
            raise SensorException(e, sys)
