import os,sys
import pandas as pd
from scipy.stats import ks_2samp

from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import read_yaml_file, write_yaml_file

class DataValidation:
    """
    This class is used for the Data Validation.
    """
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_config:DataValidationConfig,):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)

    def validate_number_of_columns(self, dataframe:pd.DataFrame)->bool:
        """
        This method is used to validate the number of columns.

        Args:
            dataframe (pd.DataFrame): dataframe

        Raises:
            SensorException: raises the exception.

        Returns:
            bool: True or false.
        """
        try:
            # number of columns.
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Data frame has columns:{len(dataframe.columns)}")
            # If length of data frame columns is equal to number of columns return True otherwise, False.
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise SensorException(e, sys)

    def is_numerical_column_exist(self, dataframe:pd.DataFrame)->bool:
        """
        This function is used to whether the numerical columns is there or not.

        Args:
            dataframe (pd.DataFrame): dataframe

        Raises:
            SensorException: raises the exception error.

        Returns:
            bool: True or False.
        """
        try:
            # numerical columns.
            numerical_columns = self._schema_config["numerical_columns"]
            # taking the dataframe columns.
            dataframe_columns = dataframe.columns
            numerical_col_present = True
            missing_numerical_columns = list()
            # Iterating the each numerical column.
            for numerical_col in numerical_columns:
                # If numerical col not in data frame then give false and appending the numerical col.
                if numerical_col not in dataframe_columns:
                    numerical_col_present = False
                    missing_numerical_columns.append(numerical_col)
            logging.info(f"Missing numerical columns:[{missing_numerical_columns}]")
            return numerical_col_present

        except Exception as e:
            raise SensorException(e, sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        """
        This method is used to read the data through pandas.

        Args:
            file_path (str): path of the file.

        Raises:
            SensorException: raises the exception error.

        Returns:
            pd.DataFrame: reading the dataframe.
        """
        try:
            # reading the data through pandas.
            return pd.read_csv(file_path)

        except Exception as e:
            raise SensorException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold = 0.5) -> bool:
        """
        This method is used to detect the drift from dataset.

        Args:
            base_df (dataframe): base dataframe
            current_df (dataframe): current dataframe
            threshold (float, optional): _description_. Defaults to 0.5.

        Raises:
            SensorException: raises the exception error.

        Returns:
            bool: True or False
        """
        try:
            status = True
            report = {}
            # Iterating the columns from base dataframe.
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                # Performs the two-sample Kolmogorov-Smirnov test for goodness of fit.
                is_same_dist = ks_2samp(d1, d2)
                # If the threshold is less than or equal to is_same_dist_p-value returning the False otherwise false.
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                # appending the each col p_value and drift_status into dictionary.
                report.update({column:{"p_value":float(is_same_dist.pvalue), "drift_status":is_found}})
            drift_report_file_path =self.data_validation_config.drift_report_file_path
            # create directory.
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            # writing the yaml file data
            write_yaml_file(file_path=drift_report_file_path, content=report)
            return status
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_validation(self, )->DataValidationArtifact:
        """
        This method is used to initiate the data validation.

        Raises:
            Exception: displaying the message
            SensorException: raises exception

        Returns:
            DataValidationArtifact: Data Validation Artifact.
        """
        try:
            error_message = ""
            train_file_path = self.data_ingestion_artifact.training_file_path
            test_file_path = self.data_ingestion_artifact.testing_file_path
            # Reading data from train and test file location.
            train_data_frame = DataValidation.read_data(train_file_path)
            test_data_frame = DataValidation.read_data(test_file_path)

            # validate number of columns for train and test.
            status = self.validate_number_of_columns(dataframe=train_data_frame)
            if not status:
                error_message = f"{error_message}Train dataframe does not contain all columns.\n"

            status = self.validate_number_of_columns(dataframe=test_data_frame)
            if not status:
                error_message = f"{error_message}Test dataframe does not contain all columns.\n"

            # validate numerical columns.
            status = self.is_numerical_column_exist(dataframe=train_data_frame)
            if not status:
                error_message = f"{error_message}Train dataframe does not contain all numerical columns.\n"
            status = self.is_numerical_column_exist(dataframe=test_data_frame)
            if not status:
                error_message = f"{error_message}Test dataframe does not contain all numerical columns.\n"
            if len(error_message)>0:
                raise Exception(error_message)

            # checking the datadrift(which means only to check the distribution of two datasets whether they belongs to same or not).
            status = self.detect_dataset_drift(base_df=train_data_frame, current_df=test_data_frame)

            # Creating the data validation artifacts.
            data_validation_artifact = DataValidationArtifact(validation_status=status, valid_train_file_path=self.data_ingestion_artifact.training_file_path, valid_test_file_path = self.data_ingestion_artifact.testing_file_path, invalid_train_file_path=self.data_validation_config.invalid_train_file_path, invalid_test_file_path=self.data_validation_config.invalid_test_file_path, drift_report_file_path=self.data_validation_config.drift_report_file_path)
            # data_validation_artifact = DataValidationArtifact(validation_status=status, valid_train_file_path=self.data_ingestion_artifact.training_file_path, valid_test_file_path = self.data_ingestion_artifact.testing_file_path, invalid_train_file_path=None, invalid_test_file_path=None, drift_report_file_path=self.data_validation_config.drift_report_file_path)
            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise SensorException(e, sys)
