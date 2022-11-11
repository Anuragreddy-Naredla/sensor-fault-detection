import sys

def error_message_details(error, error_detail:sys):
    # we are extracting the error_details information.
    _,_,exc_tb = error_detail.exc_info()
    # extracting the filename.
    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = "Error Occured Python Script name [{0}] line number [{1}] error message[{2}]".format(file_name, exc_tb.tb_lineno, str(error))

    return error_message

class SensorException(Exception):
    def __init__(self, error_message, error_detail:sys):
        """
        This class is used to return the error message in string format.

        Args:
            error_message (_type_): _description_
            error_detail (_type_): _description_
        """

        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_detail=error_detail)

        def __str__(self):
            return self.error_message