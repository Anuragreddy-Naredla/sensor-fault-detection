
import os,sys
from xgboost import XGBClassifier

from sensor.utils.main_utils import load_numpy_array_data
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.ml.metric.classification_metric import get_classification_score
from sensor.ml.model.estimator import SensorModel
from sensor.utils.main_utils import save_object, load_object



class ModelTrainer:
    """
    This class is used to train the model.
    """
    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact, ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys) from e


    def train_model(self,x_train, y_train):
        """
        This method is used to train the model.

        Args:
            x_train (data): data of x_train i.e, features
            y_train (data): data of y_train i.e, label

        Raises:
            SensorException: raises the exception.

        Returns:
            object: classifier object.
        """
        try:
            # Initiating the XGBClassifier.
            xgb_clf = XGBClassifier()
            # fitting the x_train and y_train
            xgb_clf.fit(x_train, y_train)
            return xgb_clf
        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_model_trainer(self, ):
        """
        This method is used to initiate the model training.

        Raises:
            Exception: raising the small error message.
            Exception: raising the small error message.
            SensorException: raises the exception

        Returns:
            _type_: _description_
        """
        try:
            # Getting the transformed train and test file path from data_transformation_artifact.
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            # Loading the training numpy array testing numpy array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            # differentiating the x_train,y_train,x_test,y_test features.
            x_train,y_train,x_test,y_test = (train_arr[:, :-1], train_arr[:, -1], test_arr[:,:-1], test_arr[:, -1])

            # training the model.
            model = self.train_model(x_train=x_train, y_train=y_train)
            # predicting the x_train and x_test from trained model.
            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)
            # claculating the classification score between actual and predicted labels.
            classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)
            if classification_train_metric.f1_score < self.model_trainer_config.expected_accuracy:
                raise Exception("Trained Model is not good to provide expected accuracy.")
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)

            # checking overfitting and underfitting if we will be these two cases rejecting the model.
            diff = abs(classification_train_metric.f1_score - classification_test_metric.f1_score)
            if diff > self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception("Model is not good try to do more experimentation.")
            # loading the obj.
            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)
            sensor_model = SensorModel(preprocessor=preprocessor, model=model)
            save_object(self.model_trainer_config.trained_model_file_path, obj = sensor_model)

            # Model Trainer Artifact.
            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path, train_metric_artifact=classification_train_metric, test_metric_artifact=classification_test_metric)

            logging.info(f"Model trainer artifact:{model_trainer_artifact}")

            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys) from e