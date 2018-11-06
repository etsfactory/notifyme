from flask import Flask, Response
from flask_restful import Resource, request
from marshmallow import pprint

from bussiness.users import UsersHandler, UserSchema
from bussiness.subscriptions import SubscriptionsHandler
from bussiness.bus_filters import BusFiltersHandler, BusFilterSchema

import utils.json_parser as json_parser

users = UsersHandler()
subscriptions = SubscriptionsHandler()
filters = BusFiltersHandler()
user_schema = UserSchema()
bus_filter_schema = BusFilterSchema()


class UsersView(Resource):
    """
    Handles users list endpoints /users/
    """

    def get(self):
        """
        Get users from the db
        """
        response = json_parser.to_json_list(users.get())
        return response

    def post(self):
        """
        Create user and stores in the db
        """
        json_data = request.get_json(force=True)
        users = []
        if not json_data:
            return {'message': 'No input data provided'}, 400
        if isinstance(json_data, list):

            for user in json_data:
                response, http_code = self.insert_user(user)
                users.append(user)

        else:
            response, http_code = self.insert_user(json_data)
            users.append(json_data)

        return response, http_code

    def insert_user(self, data):

        result, errors = user_schema.load(data)
        if errors:
            return errors, 422

        users.insert(result)
        return data, 201


class UserView(Resource):
    """
    Specific user endpoints /users/id
    """

    def get(self, user_id):
        """
        Get specific user from the db
        """
        response = json_parser.to_json_list(users.get(user_id))
        return response

    def put(self, user_id):
        """
        Update user passing an id
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        result, errors = user_schema.load(json_data)
        if errors:
            return errors, 422

        users.edit(result, user_id)
        return result

    def delete(self, user_id):
        """
        Delete user from the db passing an user id
        """
        users.delete(user_id)
        response = {'deleted': True}
        return response


class UserFiltersView(Resource):
    """
    Specific user bus filters /users/id/bus_filters
    """

    def get(self, user_id):
        """
        Get user bus filters
        """
        user = users.get(user_id)
        bus_filters = subscriptions.get_filters_by_user(user)
        response = json_parser.to_json_list(bus_filters)
        return response

    def post(self, user_id):
        """
        Add bus filter to an user 
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        result, errors = bus_filter_schema.load(json_data)
        if errors:
            return errors, 422

        bus_filter_id, not_exits = filters.search(result)

        if not_exits:
            bus_filter_id = filters.insert(result)['generated_keys'][0]

        subscription = {'user_id': user_id, 'filter_id': bus_filter_id}
        subscriptions.insert(subscription)

        return result
