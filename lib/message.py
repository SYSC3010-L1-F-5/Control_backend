"""

    This class handles the messages send to the frontend, 
    logging, error and other devices
    Author: Haoyu Xu

    200: HTTP OK
    401: HTTP Unauthorized
    404: HTTP Not Found
    50x: Internal Server Error

"""
from functools import wraps
import time

class Message:

    def __init__(self):
        self.app = None

    def response(self, func):
        """
        
            Changes the message to fit the structure

            Todos:
                - deal with errors
        
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            original, status_code = func(*args, **kwargs)
            result = {
                "message": original,
                "status_code": status_code,
                "error": "",
                "time": int(time.time() * 1000)
            }
            return result
        return wrapper
