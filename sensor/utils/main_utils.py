import os,sys
import yaml
import numpy as np
import dill

from sensor.exception import SensorException
from sensor.logger import logging

def read_yaml_file(file_path:str)->dict:
    """
    This function is used for the reading the yaml file.

    Args:
        file_path (str): path of the file to read

    Raises:
        SensorException: raises the exception error.

    Returns:
        dict: dictionary
    """
    try:
        # opening the yaml file and reading the yaml file.
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SensorException(e, sys) from e

def write_yaml_file(file_path:str, content:object, replace:bool = False)->None:
    """
    This function is used to write the yaml file.

    Args:
        file_path (str): path of the where we have to write the yaml file.
        content (object): content of data to dump.
        replace (bool, optional): _description_. Defaults to False.

    Raises:
        SensorException: raises the exception error.
    """
    try:
        # if any old file is there it will remove.
        if replace:
            # if file is availabe remove that file
            if os.path.exists(file_path):
                os.remove(file_path)
        # create new dir
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # dumping the content into yaml file
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise SensorException(e, sys) from e


def save_numpy_array_data(file_path:str, array:np.array):
    """
    This is function is used to saving the numpy array data.

    Args:
        file_path (str): path of the file.
        array (np.array): numpy array data.

    Raises:
        SensorException: raises the exception.
    """
    try:
        dir_path = os.path.dirname(file_path)
        # creating the dir
        os.makedirs(dir_path, exist_ok=True)
        # opening the filepath and write the numpy array data nto file.
        with open(file_path,"wb") as file_obj:
            # saving the numpy array.
            np.save(file_obj, array)
    except Exception as e:
        raise SensorException(e, sys) from e

def load_numpy_array_data(file_path:str):
    """
    This function is used to load the numpy array data.

    Args:
        file_path (str): path of the file.

    Raises:
        SensorException: raises the exception.

    Returns:
        obj: loading the numpy obj.
    """
    try:
        # loading the data from given file path.
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e

def save_object(file_path: str, obj: object):
    """
    This function is used for the saving the object.

    Args:
        file_path (str): path of the file.
        obj (object): object.

    Returns: dumping the data.

    Raises:
        SensorException: raises the exception.
    """
    logging.info("Entered the save object method of Main utils Class")
    try:
        # creating the directory.
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # writing the data in the form of pickle format by dill module.
        with open(file_path, "wb") as file_obj:
            # dumping the data.
            dill.dump(obj, file_obj)
        logging.info("Exited the save object method of mainutils class")
    except Exception as e:
        raise SensorException(e, sys) from e

def load_object(file_path: str):
    """
    The function is used for loading the object.

    Args:
        file_path (str): path of the file.

    Raises:
        Exception: error message saying that the file is not there.
        SensorException: raises the exception.

    Returns:
        data: loading the data
    """
    logging.info("Entered the save object method of Main utils Class")
    try:
        # If file path doest not exists raise the message.
        if not os.path.exists(file_path):
            raise Exception("The File:{file_path} is not exists")
        # opening the file then reading the file.
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e
