"""

    All event related methods will be here
    Author: Haoyu Xu

"""

from flask_restful import Resource

class Event(Resource):

    def __init__(self):
        self.debug = False

    def get(self):
        return {'hello': 'event'}