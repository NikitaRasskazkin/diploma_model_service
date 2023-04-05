"""Methods and datastructure for recognizing paraphrased sentences in the text API"""

import time

from flask_restful import Resource, fields, marshal_with
from pydantic import BaseModel

from common.api_utils import build_success_schema, json_success_response, json_request
from ..recognition_model.manager import RecognitionManager


post_response_schema = build_success_schema({
    'version': fields.String,
    'weights_slug': fields.String,
    'source_text': fields.String,
    'recognition': fields.List(fields.Nested({
        'sentence': fields.String,
        'is_paraphrase': fields.Boolean,
        'probability': fields.Float,
    })),
    'recognition_time': fields.Float,
})


class PostRequest(BaseModel):
    """Post request JSON body"""
    text: str


class Recognition(Resource):
    """Methods for recognizing paraphrased sentences in the text"""

    @staticmethod
    @json_request(PostRequest)
    @marshal_with(post_response_schema)
    def post(data: PostRequest):
        """Perform recognition of paraphrased sentences in the text"""
        text = data.text
        start_time = time.time()
        result = RecognitionManager.model.get_recognition(text)
        recognition_time = time.time() - start_time
        return json_success_response({
            'version': RecognitionManager.model.version,
            'weights_slug': RecognitionManager.model.weights_slug,
            'source_text': text,
            'recognition': result,
            'recognition_time': recognition_time,
        })
