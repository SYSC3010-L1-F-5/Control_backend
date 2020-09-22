"""

    This class handles the messages send to the frontend, 
    logging, error and other devices
    Author: Haoyu Xu

    200: HTTP OK
    401: HTTP Unauthorized
    404: HTTP Not Found
    50x: Internal Server Error

"""
from flask import jsonify
from functools import wraps
import time

class Api:

    def __init__(self):
        self.app = None

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
                "message": original,
                "status_code": 200,
                "error": "",
                "time": int(time.time() * 1000)
            }
            return jsonify(result)
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