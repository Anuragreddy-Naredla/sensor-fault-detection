
import os
from datetime import datetime

from sensor.constant import training_pipeline


class TrainingPipelineConfig:
    """
    This class is used to initialize the TrainingPipelineConfigurations from __init__.py file.
    """
    def __init__(self, timestamp = datetime.now()):

        timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name:str = training_pipeline.PIPELINE_NAME
        self.artifact_dir: str = os.path.join(training_pipeline.ARTIFACT_DIR, timestamp)
        self.timestamp: str = timestamp


class DataIngestionConfig:
    """
    This class is used to saving initialize data ingestion configurations.
    """

    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        # Creating the data ingestion folder.
        self.data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME)
        # creating the path to store the data in csv file.
        self.feature_store_file_path: str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME)
        # creating the path for train data.
        self.training_file_path:str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME)
        # creating the path for test data.
        self.testing_file_path:str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME)
        # splitting the data in the ratio format.
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        # taking the collection name.
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME

class DataValidationConfig:
    """
    This class is used to initialize the Data validation configurations.
    """
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        # creating the data validation folder.
        self.data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)
        # creating the data validation directory.
        self.valid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        # creating the data invalid directory.
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        # creating the valid train file path
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        # create the valid test file path.
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
        # creating the invalid train file path.
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        # creating the invalid test file path.
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)
        # creating the drift report file path.
        self.drift_report_file_path: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)

class DataTransformationConfig:
    """
    This class is used to initialize the Data transformation configurations.
    """
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        # creating the data transformation directory.
        self.data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        # creating the data transformation train file path.
        self.transformed_train_file_path: str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"))
        # creating the data transformation test file path.
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, training_pipeline.TEST_FILE_NAME.replace("csv", "npy"))
        # creating the transformed object file path.
        self.transformed_object_file_path:str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, training_pipeline.PREROCESSING_OBJECT_FILE_NAME)

class ModelTrainerConfig:
    """
    This class is used to initialize the model trainer configurations.
    """

    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        # creating the model trainer directory.
        self.model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINER_DIR_NAME)
        # creating the trained model file path.
        self.trained_model_file_path: str = os.path.join(self.model_trainer_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR, training_pipeline.MODEL_FILE_NAME)
        # creating the expected accuracy variable.
        self.expected_accuracy: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        # creating the variable for overfitting and underfitting threshold.
        self.overfitting_underfitting_threshold: float = training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD

class ModelEvaluationConfig:
    """
    This class id used to initialize the model evaluation configurations.
    """
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        # creating the model evaluation directory.
        self.model_evaluation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_EVALUATION_DIR_NAME)
        # creating the report file path.
        self.report_file_path: str = os.path.join(self.model_evaluation_dir, training_pipeline.MODEL_EVALUATION_REPORT_FILE_NAME)
        # creating the variable of model evaluation change threshold.
        self.change_threshold: str = training_pipeline.MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE

class ModelPusherConfig:
    """
     This class is used to initialize the model pusher configurations.
    """
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        # creating the model pusher directory.
        self.model_pusher_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_PUSHER_DIR_NAME)
        # creating the model file path.
        self.model_file_path: str = os.path.join(self.model_pusher_dir, training_pipeline.MODEL_FILE_NAME)
        # creating the timestamp variable.
        timestamp = round(datetime.now().timestamp())
        # creating the saved model path diretory.
        self.saved_model_path: str = os.path.join(training_pipeline.SAVED_MODEL_DIR, f"{timestamp}", training_pipeline.MODEL_FILE_NAME)
