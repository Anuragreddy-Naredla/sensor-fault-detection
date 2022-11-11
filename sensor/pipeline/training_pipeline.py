
import sys

from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelPusherConfig, ModelEvaluationConfig, ModelTrainerConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelEvaluationArtifact, ModelTrainerArtifact
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher
from sensor.constant.s3_bucket import TRAINING_BUCKET_NAME
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.cloud_storage.S3Syncer import S3Sync


class TrainPipeline:
    """
    This Class is used to train the entitire pipeline of ML model.
    """
    is_pipeline_running = False
    def __init__(self, ):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()
        # self.training_pipeline_config = training_pipeline_config

    def start_data_ingestion(self)->DataIngestionArtifact:
        """
        This method is used to start the data ingestion of ML pipeline.

        Raises:
            SensorException: raises exception error

        Returns:
            DataIngestionArtifact: Artifact of Data Ingestion.
        """
        try:
            # Creating data_ingestion_configuration.
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data ingestion")
            # Creating the object of data ingestion component where we passed data_ingestion_configuration.
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            # Output of Data ingestion artifact.
            data_ingest_artifact = data_ingestion.initiate_data_ingestion()
            # Logging the data_ingest_artifact.
            logging.info(f"Data ingestion completed and artifact:{data_ingest_artifact}")
            return data_ingest_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact):
        """
        This method is used to start the Data_Validation of ML.

        Args:
            data_ingestion_artifact (DataIngestionArtifact): class of DataIngestionArtifact

        Raises:
            SensorException: raises exception error

        Returns:
            data_validation_artifact: Data Validation artifact
        """
        try:
            # Creating the obj of DataValidationConfig Class.
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            # Creating the object of DataValidation.
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)
            # Initiating the data_validation function which returns data_validation_artifact.
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def start_data_transformation(self, data_validation_artifact:DataValidationArtifact):
        """
        This method is used to start the data tranformation of ML.

        Args:
            data_validation_artifact (DataValidationArtifact): Class of DataValidationArtifact

        Raises:
            SensorException: raises exception error

        Returns:
            data_transformation_artifact: Data Transformation Artifact.
        """
        try:
            # creating the obj of DataTransformationConfig.
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            # Creating the object of DataTransformation.
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config = data_transformation_config)
            # Initiating the data_transformation function which returns the data_transformation_artifact.
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys)

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact,):
        """
        This method is used to start the model training.

        Args:
            data_transformation_artifact (DataTransformationArtifact): class of DataTransformationArtifact.

        Raises:
            SensorException: raises Exception error

        Returns:
            model_trainer_artifact: Model Trainer Artifact.
        """
        try:
            # Creating the obj of ModelTrainerConfig.
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            # Creating the object of ModelTrainer.
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
            # Initiating the model trainer function which returns the model_trainer_artifact.
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def start_model_evaluation(self, data_validation_artifact: DataValidationArtifact, model_trainer_artifact:ModelTrainerArtifact):
        """
        This method is used to start the model evaluation.

        Args:
            data_validation_artifact (DataValidationArtifact): Class of DataValidationArtifact.
            model_trainer_artifact (ModelTrainerArtifact): class of ModelTrainerArtifact.

        Raises:
            SensorException: raises Exception error.

        Returns:
            model_eval_artifact: Model Evaluation Artifact
        """
        try:
            # creating the obj of ModelEvaluationConfig.
            model_eval_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
            # Creating the object of ModelEvaluation.
            model_eval = ModelEvaluation(model_evaluation_config=model_eval_config, data_validation_artifcat=data_validation_artifact, model_trainer_artifact=model_trainer_artifact)
            # Initiating the model evaluation function which returns the model_evaluation_artifact.
            model_eval_artifact = model_eval.initiate_model_evaluation()
            return model_eval_artifact

        except Exception as e:
            raise SensorException(e, sys)

    def start_model_pusher(self, model_eval_artifact:ModelEvaluationArtifact):
        """
        This method is used to start the model pusher.

        Args:
            model_eval_artifact (ModelEvaluationArtifact): Class of ModelEvaluationArtifact

        Raises:
            SensorException: raises Exception error.

        Returns:
            model_pusher_artifact: Model Pusher Artifact.
        """
        try:
            # Creating the object of ModelPusherConfig
            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            # Creating obj of Model Pusher
            model_pusher = ModelPusher(model_pusher_config=model_pusher_config, model_eval_artifact = model_eval_artifact)
            # Initiating the model pusher function which returns the model pusher artifact.
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys)
    def sync_artifact_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir, aws_bucket_url=aws_buket_url)
        except Exception as e:
            raise SensorException(e,sys)

    def sync_saved_model_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/{SAVED_MODEL_DIR}"
            self.s3_sync.sync_folder_to_s3(folder=SAVED_MODEL_DIR, aws_bucket_url=aws_buket_url)
        except Exception as e:
            raise SensorException(e,sys)

    def run_pipeline(self):
        """
        This methood is used to run the entire pipeline of ML model by using the above functions.

        Raises:
            Exception: message
            SensorException: raises Exception error.
        """
        try:
            TrainPipeline.is_pipeline_running = True
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            model_eval_artifact = self.start_model_evaluation(data_validation_artifact=data_validation_artifact,model_trainer_artifact=model_trainer_artifact)
            if not model_eval_artifact.is_model_accepted:
                raise Exception("Trained Model is not better than the best model")
            model_pusher_artifact = self.start_model_pusher(model_eval_artifact=model_eval_artifact)
            TrainPipeline.is_pipeline_running = False
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
        except Exception as e:
            self.sync_artifact_dir_to_s3()
            TrainPipeline.is_pipeline_running = False
            raise SensorException(e, sys)
