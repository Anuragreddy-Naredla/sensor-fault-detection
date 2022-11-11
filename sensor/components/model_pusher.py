import sys,os
import shutil

from sensor.entity.artifact_entity import  ModelEvaluationArtifact, ModelPusherArtifact
from sensor.entity.config_entity import ModelPusherConfig
from sensor.exception import SensorException
from sensor.logger import logging

class ModelPusher:
    def __init__(self, model_pusher_config:ModelPusherConfig,model_eval_artifact:ModelEvaluationArtifact, ):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_eval_artifact = model_eval_artifact
        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_model_pusher(self, ):
        try:
            trained_model_path = self.model_eval_artifact.trained_model_path

            # creating the model pusher directory.
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst = model_file_path)

            # saved model dir
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst = saved_model_path)

            # Prepare the Artifact.
            model_pusher_artifact = ModelPusherArtifact(saved_model_path=saved_model_path, model_file_path=model_file_path)
            logging.info("Model Pusher Artifact:{model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
