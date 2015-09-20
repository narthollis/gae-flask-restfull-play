from __future__ import absolute_import, division, print_function
from flask_restful import Resource, fields, marshal_with, request
from main import api_v1


@api_v1.resource('/test/', '/test/<string:item_id>', endpoint='api.test')
class TestEndpoint(Resource):
    def get(self, item_id=None):
        if item_id is None:
            return self.get_all()
        else:
            return self.get_one(item_id)

    def get_all(self):
        return {
            'test': 'value'
        }

    def get_one(self, item_id):
        return {'error': 'Item not found.'}, 404
