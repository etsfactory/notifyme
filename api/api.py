import json

from flask import Flask
from flask_restful import Api
from api.api_users import UsersView, UserView

import threading

class ApiHandler(threading.Thread):
    def __init__(self):
        print('Staring API')
        super(ApiHandler, self).__init__()
    
    def run(self):
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(UsersView, '/users')
        api.add_resource(UserView, '/users/<string:user_id>')
        app.run()
