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
        self.messages = {
            "200": "HTTP 200 OK",
            "401": "HTTP Unauthorized",
            "404": "HTTP Not Found",
            "500": "Internal Server Error"
        }

    def response(self, func):
        """
        
            Changes the message to fit the structure

            Todos:
                - deal with errors
        
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            original, status_code = func(*args, **kwargs) or None, 500
            result = {
                "message": self.message(status_code, original),
                "status_code": status_code,
                "time": int(time.time() * 1000)
            }
            return result, status_code
        return wrapper

    def message(self, code, message=None):
        return message or self.messages[str(code)]
            
