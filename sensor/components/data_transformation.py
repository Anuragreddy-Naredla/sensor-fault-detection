import sys, os
import numpy as np
import pandas as pd

from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact

from sensor.entity.config_entity import DataTransformationConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.ml.model.estimator import TargetValueMapping
from sensor.utils.main_utils import save_numpy_array_data, save_object

class DataTransformation:
    """
    This class consists the functions of data transformation which is used to transform the data.
    """
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise SensorException(e, sys) from e

    @staticmethod
    def read_data(file_path):
        """
        This method is used to read the data through pandas.

        Args:
            file_path (str): path of the file.

        Raises:
            SensorException: raises the exception error.

        Returns:
            Dataframe: pandas dataframe.
        """
        try:
            # reading the data through pandas.
            return pd.read_csv(file_path)

        except Exception as e:
            raise SensorException(e, sys) from e

    @classmethod
    def get_data_transformer_object(cls):
        """
        This method is used to get the data transformer object.


        Raises:
            SensorException: raises the exception error.

        Returns:
            obj : preprocesser data obj
        """
        try:
            # Initiating the robust scaler
            robust_scaler = RobustScaler()
            # Intiating the simple imputer.
            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)
            # If there any missing values is there update with 0 "robust scaler": keeps every feature in same range and handles outliers.
            preprocesser = Pipeline(steps=[("Imputer", simple_imputer), ("RobustScaler", robust_scaler)])
            return preprocesser

        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_data_transformation(self,):
        """
        This method is used to initiate the data transformations.

        Raises:
            SensorException: raises the exception error.

        Returns:
            Data Transformation Artifact: Artifact of data transformation.
        """
        try:
            # reading the valid train and test data.
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            preprocessor = self.get_data_transformer_object()
            # Getting the input and target features from train data.
            target_feature_train_df = train_df[TARGET_COLUMN]
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis = 1)
            target_feature_train_df = target_feature_train_df.replace(TargetValueMapping().to_dict())
            # Getting the input and target features from test data.
            target_feature_test_df = test_df[TARGET_COLUMN]
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis = 1)
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict())
            # fitting and transforming the train data.
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            # fitting and transforming the test data.
            preprocessor_object = preprocessor.fit(input_feature_test_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)
            # Performing the SMOTE to balance the data based on target labels.
            smt = SMOTETomek(sampling_strategy="minority")
            input_feature_train_final, target_feature_train_final = smt.fit_resample(transformed_input_train_feature, target_feature_train_df)
            input_feature_test_final, target_feature_test_final = smt.fit_resample(transformed_input_test_feature, target_feature_test_df)
            # concatenating the train and test features.
            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]
            # saving the data in the format of numpy.
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array = train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array = test_arr)
            # saving the object.
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
            data_transformation_artifact = DataTransformationArtifact(transformed_object_file_path=self.data_transformation_config.transformed_object_file_path, transformed_train_file_path=self.data_transformation_config.transformed_train_file_path, transformed_test_file_path=self.data_transformation_config.transformed_test_file_path)
            logging.info(f"Data transformation artifact:{data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys ) from e