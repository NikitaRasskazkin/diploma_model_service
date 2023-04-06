"""Service entry point"""

from flask import Flask
from flask_restful import Api

import common.settings as settings
from service.urls import add_resources


app = Flask(__name__)
api = Api(app)
add_resources(api)


if __name__ == '__main__':
    app.run(debug=settings.DEBUG, port=settings.PORT)
