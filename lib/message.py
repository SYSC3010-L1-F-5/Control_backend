"""

    This class handles the messages send to the frontend, 
    logging, error and other devices
    Author: Haoyu Xu

    200: HTTP OK
    401: HTTP Unauthorized
    404: HTTP Not Found
    500: Internal Server Error

"""
from functools import wraps
import time

class Message:

    def __init__(self):
        self.app = None
        self.messages = {
            "200": "HTTP 200 OK",
            "401": "HTTP Unauthorized",
            "403": "Forbidden",
            "404": "HTTP Not Found",
            "500": "Internal Server Error"
        }

    def response(self, func):
        """
        
            Changes the message to fit the structure
        
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            original, status_code = func(*args, **kwargs)
            result = {
                "message": self.message(status_code, original),
                "status_code": status_code,
                "time": int(time.time() * 1000)
            }
            return result, status_code
        return wrapper

    def errorhandler(self, status_code):
        """

            Response proper error formate

        """
        result = {
            "message": self.message(status_code, ""),
            "status_code": status_code,
            "time": int(time.time() * 1000)
        }
        return result

    def message(self, code, message):
        if message == "":
            message = self.messages[str(code)]
        return message
            
