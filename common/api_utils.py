"""Utils and shortcuts to simplify working with simplifying and standardizing API methods"""

from typing import Dict, Any, Callable, TypeVar, Type, Tuple
from datetime import datetime

import pytz
from flask_restful import fields
from flask import request
from pydantic import BaseModel, ValidationError


def timezone_now() -> datetime:
    """get datetime with utc timezone"""
    return datetime.utcnow().replace(tzinfo=pytz.utc)


def build_success_schema(data_schema: Dict[str, fields.Raw]) -> Dict[str, fields.Raw]:
    """Insert data schema into standard response success schema and return it"""
    return {
        'success': fields.Boolean,
        'message': fields.String,
        'errors': fields.List(fields.String),
        'dttm': fields.DateTime(dt_format='iso8601'),
        'data': fields.Nested(data_schema),
    }


def json_success_response(data) -> Dict[str, Any]:
    """Standard JSON response"""
    return {
        'success': True,
        'message': 'OK',
        'errors': [],
        'dttm': timezone_now(),
        'data': data,
    }


def json_bad_request(message: str, errors: list) -> Tuple[Dict[str, Any], int]:
    """JSON Bad Request response"""
    return {
        'success': False,
        'message': message,
        'errors': errors,
        'dttm': timezone_now().isoformat(),
        'data': None,
    }, 400


D = TypeVar('D', bound=Type[BaseModel])
R = TypeVar('R')


def json_request(request_body: D) -> Callable[..., R]:
    """
        Decorator to API method that contain JSON body.
        Extracts the JSON body from the request, validates the fields according to request_body,
        and converts to the request_body request data structure.
        The received data structure of the request passes the first arguments to the function.
        Arguments to the resulting function can only be passed as kvargs.
    """
    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        def wrapper(**kwargs) -> R:
            try:
                data = request_body(**request.json)
            except ValidationError as e:
                return json_bad_request('JSON body validation error', e.errors())
            return func(data, **kwargs)
        return wrapper
    return decorator
