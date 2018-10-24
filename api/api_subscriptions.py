from flask import Flask, Response
from flask_restful import Resource, Api, request
from marshmallow import pprint

from bussiness.users import UsersHandler
from bussiness.users import User
from bussiness.bus_filters import BusFiltersHandler
from bussiness.bus_filters import BusFilter

from bussiness.subscriptions import SubscriptionsHandler
from bussiness.subscriptions import SubscriptionSchema
from bussiness.subscriptions import Subscription

import utils.json_parser as json_parser

users = UsersHandler()
filters = BusFiltersHandler()
subscriptions = SubscriptionsHandler()
subscription_schema = SubscriptionSchema()

class SubscriptionsView(Resource):

    def get(self):
        """
        Get subscriptions from the db
        """
        response = json_parser.to_json_list(subscriptions.get())
        return response

    def post(self):
        """
        Create subscription
        """
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        result, errors = subscription_schema.load(json_data)
        if errors:
            return errors, 422

        subscription = Subscription(result['user_id'], result['filter_id'])
        subscriptions.insert(subscription)
        response = json_parser.to_json_list(subscription)
        return response, 201

class SubscriptionView(Resource):

     def delete(self, subscription_id):
        """
        Delete subscription by his id
        """
        subscription = subscriptions.get(subscription_id)
        subscriptions.delete(subscription)
        response = json_parser.to_json_list(subscription)
        return response