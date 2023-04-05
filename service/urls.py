"""Contains functions for binding resources URLs"""

from flask_restful import Api

from common.settings import URLS_ROOT
from .resources_views import test, recognition


def __add_url_prefix(url: str) -> str:
    """Add standard prefix to url which contains the url version"""
    return URLS_ROOT + url


def add_resources(api: Api) -> Api:
    """Adds resources URLs to api"""
    api.add_resource(test.Test, __add_url_prefix('/test/<int:test_id>'), endpoint="test")
    api.add_resource(test.TestsSet, __add_url_prefix('/test'), endpoint="test_set")
    api.add_resource(recognition.Recognition, __add_url_prefix('/recognition'), endpoint="recognition")
    return api
