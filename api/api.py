import json

from flask import Flask
from flask_restful import Api
from api.api_users import UsersView, UserView
from api.api_bus_filters import BusFiltersView, BusFilterView

import threading

class ApiHandler(threading.Thread):
    def __init__(self):
        print('Staring API')
        super(ApiHandler, self).__init__()
    
    def run(self):
        app = Flask(__name__)
        api = Api(app)
        
        api.add_resource(UsersView, '/users')
        api.add_resource(UserView, '/user/<string:user_id>')

        api.add_resource(BusFiltersView, '/bus_filters')
        api.add_resource(BusFilterView, '/bus_filter/<string:bus_filter_id>')

        app.run()
