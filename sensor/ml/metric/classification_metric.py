import os,sys
from sklearn.metrics import f1_score, precision_score, recall_score

from sensor.entity.artifact_entity import ClassificationMetricArtifact
from sensor.exception import SensorException

def get_classification_score(y_true,y_pred):
    """
    This method is used to gettting the classification scores from true and predicted labels.

    Args:
        y_true (numerical): Actual labels
        y_pred (numerical): predicted labels.

    Raises:
        SensorException: raises the exception error.

    Returns:
        obj: classification metric
    """
    try:
        # calculating the f1_score, recall_score, precision_score between actual and predicted labels.
        model_f1_score = f1_score(y_true,y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score = precision_score(y_true,y_pred)
        classification_metric = ClassificationMetricArtifact(f1_score=model_f1_score, precision_score=model_precision_score, recall_score=model_recall_score)
        return classification_metric
    except Exception as e:
        raise SensorException(e, sys) from e