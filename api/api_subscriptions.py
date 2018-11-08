from flask import Flask, Response
from flask_restful import Resource, request
from marshmallow import pprint

from bussiness.users import UsersHandler
from bussiness.bus_filters import BusFiltersHandler
from bussiness.subscriptions import SubscriptionsHandler, SubscriptionSchema

import utils.json_parser as json_parser


users = UsersHandler()
filters = BusFiltersHandler()
subscriptions = SubscriptionsHandler()
subscription_schema = SubscriptionSchema()


class SubscriptionsView(Resource):
    """
    Subscriptions endpoints /subscriptions/
    """

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
        subscriptions = []
        if not json_data:
            return {'message': 'No input data provided'}, 400

        if isinstance(json_data, list):
            for subscription in json_data:
                response, http_code = self.insert_subscription(subscription)
                subscriptions.append(subscription)
        else:
            response, http_code = self.insert_subscription(json_data)
            subscriptions.append(json_data)

        return response, http_code

    def insert_subscription(self, data):
        """
        Insert and validate subscription. Checks if user and bus filter exits
        """
        result, errors = subscription_schema.load(data)
        if errors:
            return errors, 422

        bus_filter_exits = filters.get(result['filter_id'])
        user_exits = users.get(result['user_id'])

        if (bus_filter_exits and user_exits):
            subscription = {
                'user_id': result['user_id'], 'filter_id': result['filter_id']}
            subscriptions.insert(subscription)
        else:
            return {'message': 'Bus filter id or user filter id does not exits'}, 422


class SubscriptionView(Resource):
    """
    Specific subscriptions endpoints /subscriptions/id
    """

    def delete(self, subscription_id):
        """
        Delete subscription by his id
        """
        subscription = subscriptions.get(subscription_id)
        if subscription:
            subscriptions.delete(subscription_id)
            response = {'deleted': True}
            return response
        else:
            return {'message': 'Subscription not found'}, 404


    def put(self, subscription_id):
        """
        Update template passing his id
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        result, errors = subscription_schema.load(json_data)
        
        if errors:
            return errors, 422

        subscription = subscriptions.get(subscription_id)
        if subscription:
            subscription = {
                'user_id': result['user_id'], 'filter_id': result['filter_id'], 'template_id': result['template_id']}
            subscriptions.edit(subscription, subscription_id)
            return subscription
        else:
            return {'message': 'Subscription not found'}, 404

    def get(self, subscription_id):
        return subscriptions.get(subscription_id)
