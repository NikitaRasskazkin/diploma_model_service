"""A test resource for experiments"""

from flask import request
from flask_restful import Resource


class Test(Resource):
    """Test resource"""

    def get(self, test_id: int):
        return {
            'test': test_id,
        }


class TestsSet(Resource):
    """Set of tests resources"""
    def post(self):
        data = request.json
        return {
            'status': 'OK',
            'data': data,
        }
