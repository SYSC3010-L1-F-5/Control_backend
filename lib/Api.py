"""

    This class handles the messages send to the frontend, 
    logging, error and other devices
    Author: Haoyu Xu

"""

from functools import wraps
import time

class Api():

    def __init__(self):
        self.debug = False

    def message(self, func):
        """
        
            Changes the message to fit the structure

            Todos:
                - deal with errors
        
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            original = func(*args, **kwargs)
            result = {
                "body": original,
                "status_code": 200,
                "time": int(time.time() * 1000)
            }
            return str(result)
        return wrapper

    def logger(self, func):
        """
        
            A logger to log events

            Todos:
                - finish design
                - add runtime arguments
                - database operations
        
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            return result
        return wrapper