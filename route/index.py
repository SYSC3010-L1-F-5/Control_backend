"""

    All user related methods will be here
    Author: Haoyu Xu

"""

from flask_restful import Resource

class Index(Resource):

    def get(self):
        return {'hello': 'world'}
