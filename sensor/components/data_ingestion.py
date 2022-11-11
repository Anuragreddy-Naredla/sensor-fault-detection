
import os,sys
from pandas import DataFrame
from sklearn.model_selection import train_test_split

from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.data_access.sensor_data import SensorData
from sensor.utils.main_utils import read_yaml_file
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH

class DataIngestion:
    """
    This class consists of all the data ingestion functions.
    """
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)

    def export_data_into_feature_store(self, )->DataFrame:
        """
        This method is used to Export mongodb collection record as dataframe into feature.

        Returns:
            DataFrame: _description_
        """
        try:
            logging.info("Exporting the data from mongodb to feature store")
            sensor_data = SensorData()
            dataframe = sensor_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name, )
            # Getting the feature store filepath.
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            # creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            # exist_ok means if folder is available no need to create if folder not available create it.
            os.makedirs(dir_path, exist_ok=True)

            # Saving the data, if i not give index = False it will create one more extra col.
            dataframe.to_csv(feature_store_file_path, index = False, header = True)
            return dataframe


        except Exception as e:
            raise SensorException(e,sys)

    def split_data_as_train_test(self, dataframe:DataFrame):
        """
        This method is used to feature store dataset split into train and test file.

        Args:
            dataframe (DataFrame): dataframe
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            # spliting the train and test data.
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )

            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            # Returning the directory of training file path
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            # creating the directory.
            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train and test file path.")
            # conevrt the train and test set into csv and saving
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_data_ingestion(self, )->DataIngestionArtifact:
        """
        This function is used to initiate the data ingestion.

        Raises:
            SensorException: raises exception error.

        Returns:
            DataIngestionArtifact: Artifact of data ingestion.
        """
        try:
            # exporting the data into csv file from mongodb.
            dataframe = self.export_data_into_feature_store()
            # dropping the columns.
            dataframe = dataframe.drop(self._schema_config["drop_columns"], axis=1)
            # splitting the data into train and test data.
            self.split_data_as_train_test(dataframe=dataframe)
            # calling the data ingestion artifact.
            data_ingestion_artifact = DataIngestionArtifact(training_file_path=self.data_ingestion_config.training_file_path, testing_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
