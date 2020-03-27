"""
APi subscriptions handler
"""
from flask_restful import Resource, request

from bussiness.users import UsersHandler
from bussiness.bus_filters import BusFiltersHandler
from bussiness.subscriptions import SubscriptionsHandler, SubscriptionSchema

from utils import json_parser


users = UsersHandler()
filters = BusFiltersHandler()
subscriptions = SubscriptionsHandler()
subscription_schema = SubscriptionSchema()


class SubscriptionsView(Resource):
    """
    Subscriptions endpoints /subscriptions/
    """

    @staticmethod
    def get():
        """
        Get subscriptions from the db
        """
        response = json_parser.to_json_list(
            subscriptions.get_with_relationships())
        return response

    def post(self):
        """
        Create subscription
        """
        json_data = request.get_json(force=True)
        subscription_list = []
        if not json_data:
            return {'message': 'No input data provided'}, 400

        if isinstance(json_data, list):
            for subscription in json_data:
                response, http_code = self.insert_subscription(subscription)
                subscription_list.append(response)
                if http_code != 201:
                    return response, http_code
            return subscription_list, 201
        response, http_code = self.insert_subscription(json_data)
        if http_code != 201:
            return response, http_code

        return response, 201

    @staticmethod
    def insert_subscription(data):
        """
        Insert and validate subscription.
        Checks if user and bus filter exits
        """
        result, errors = subscription_schema.load(data)
        if errors:
            return errors, 422

        bus_filter_exits = filters.get(result['filter_id'])
        user_exits = users.get(result['user_id'])

        if (bus_filter_exits and user_exits):
            subscriptions.insert(result)
        return {
            'message': 'Bus filter id or user id does not exits'}, 422


class SubscriptionView(Resource):
    """
    Specific subscriptions endpoints /subscriptions/id
    """

    @staticmethod
    def delete(subscription_id):
        """
        Delete subscription by his id
        """
        subscription = subscriptions.get(subscription_id)
        if subscription:
            subscriptions.delete(subscription_id)
            response = {'deleted': True}
            return response
        return {'message': 'Subscription not found'}, 404

    @staticmethod
    def put(subscription_id):
        """
        Edit subscription passing his id
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        result, errors = subscription_schema.load(json_data)

        if errors:
            return errors, 422

        subscription = subscriptions.get(subscription_id)
        if subscription:
            subscriptions.edit(result, subscription_id)
            return subscription

        return {'message': 'Subscription not found'}, 404

    @staticmethod
    def get(subscription_id):
        """
        Get specific subscription by his id
        """
        return subscriptions.get(subscription_id)
