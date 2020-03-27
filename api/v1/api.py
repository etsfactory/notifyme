"""
APi handler
"""
import threading

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_restful import Api, Resource

import settings as st

from api.v1.api_users import UsersView, UserView, UserFiltersView, UserFilterView
from api.v1.api_bus_filters import (
    BusFiltersView,
    BusFilterView,
    BusFilterUsersView,
    BusFilterUserView,
    BusFilterTemplateView
)
from api.v1.api_subscriptions import SubscriptionsView, SubscriptionView
from api.v1.api_templates import TemplatesView, TemplateView, TemplatesBusFiltersView
from api.v1.api_messages import MessagesView


class ApiHandler(threading.Thread):
    """
    Handles API calls and endpoints in a thread
    """

    def __init__(self):
        st.logger.info('Staring API...')
        super(ApiHandler, self).__init__()

    def run(self):
        """
        Thread running. API initialization
        """
        app = Flask(__name__)
        api = Api(app, prefix='/v1')
        CORS(app)

        api.add_resource(UsersView, '/users')
        api.add_resource(UserView, '/users/<string:user_id>')
        api.add_resource(
            UserFiltersView, '/users/<string:user_id>/bus_filters')
        api.add_resource(
            UserFilterView,
            '/users/<string:user_id>/bus_filters/<string:bus_filter_id>')

        api.add_resource(BusFiltersView, '/bus_filters')
        api.add_resource(BusFilterView, '/bus_filters/<string:bus_filter_id>')
        api.add_resource(BusFilterUsersView,
                         '/bus_filters/<string:bus_filter_id>/users')
        api.add_resource(BusFilterUserView,
                         '/bus_filters/<string:bus_filter_id>/users/<string:user_id>')
        api.add_resource(BusFilterTemplateView,
                         '/bus_filters/<string:bus_filter_id>/templates')

        api.add_resource(SubscriptionsView, '/subscriptions')
        api.add_resource(SubscriptionView,
                         '/subscriptions/<string:subscription_id>')

        api.add_resource(TemplatesView, '/templates')
        api.add_resource(TemplateView, '/templates/<string:template_id>')
        api.add_resource(TemplatesBusFiltersView,
                         '/templates/<string:template_id>/bus_filters')

        api.add_resource(Documentation, '/spec')
        api.add_resource(MessagesView, '/messages')
        app.run(host=st.API_SERVER, port=st.API_PORT)


class Documentation(Resource):
    def get(self):
        directory = '../../specs/'
        filename = 'spec.yml'
        return send_from_directory(directory, filename, as_attachment=True)

