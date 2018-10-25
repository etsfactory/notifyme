import json

from flask import Flask
from flask_restful import Api
from api.api_users import UsersView, UserView, UserFiltersView
from api.api_bus_filters import BusFiltersView, BusFilterView, BusFilterUsersView
from api.api_subscriptions import SubscriptionsView, SubscriptionView

import threading

class ApiHandler(threading.Thread):
    def __init__(self):
        print('Staring API...')
        super(ApiHandler, self).__init__()
    
    def run(self):
        """
        Thread running. API initialization
        """
        app = Flask(__name__)
        api = Api(app)
        
        api.add_resource(UsersView, '/users')
        api.add_resource(UserView, '/users/<string:user_id>')
        api.add_resource(UserFiltersView, '/users/<string:user_id>/bus_filters')

        api.add_resource(BusFiltersView, '/bus_filters')
        api.add_resource(BusFilterView, '/bus_filters/<string:bus_filter_id>')
        api.add_resource(BusFilterUsersView, '/bus_filters/<string:bus_filter_id>/users')

        api.add_resource(SubscriptionsView, '/subscriptions')
        api.add_resource(SubscriptionView, '/subscriptions/<string:subscription_id>')

        app.run()
