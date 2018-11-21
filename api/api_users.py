from flask import Flask, Response
from flask_restful import Resource, request

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
        print('-------------------------')
        print(response)
        return response

    def post(self):
        """
        Create user and stores in the db
        """
        json_data = request.get_json(force=True)
        users_list = []
        if not json_data:
            return {'message': 'No input data provided'}, 400
        if isinstance(json_data, list):

            for user in json_data:
                response, http_code = self.check_user(user)

                if (http_code != 201):
                    return response, http_code

                users_list.append(response)
            users.insert(users_list)
            return users_list, 201

        else:
            response, http_code = self.check_user(json_data)
            if (http_code != 201):
                return response, http_code

            users.insert(response)
            return response, 201

    def check_user(self, data):

        result, errors = user_schema.load(data)
        if errors:
            return errors, 422

        print(result)
        return result, 201


class UserView(Resource):
    """
    Specific user endpoints /users/id
    """

    def get(self, user_id):
        """
        Get specific user from the db
        """

        response = users.get(user_id)

        if response:
            return response
        else:
            return {'message': 'User not found'}, 404

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

        user = users.get(user_id)
        if user:
            users.edit(result, user_id)
            return result
        else:
            return {'message': 'User not found'}, 404

    def delete(self, user_id):
        """
        Delete user from the db passing an user id
        """
        user = users.get(user_id)
        if user:
            users.delete(user_id)
            subscriptions.delete_user(user_id)
            response = {'deleted': True}
            return response
        else:
            return {'message': 'User not found'}, 404


class UserFiltersView(Resource):
    """
    Specific user bus filters /users/id/bus_filters
    """

    def get(self, user_id):
        """
        Get user bus filters
        """
        user = users.get(user_id)
        if user:
            bus_filters = subscriptions.get_filters_by_user(user)
            response = json_parser.to_json_list(bus_filters)
            return response
        else:
            return {'message': 'User not found'}, 404

    def post(self, user_id):
        """
        Add bus filter to an user
        """
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400

        if isinstance(json_data, list):
            sub_list = []
            for bus_filter in json_data:
                response, error = self.check_filter(bus_filter, user_id)
                if error:
                    return response, error
                sub_list.append(response)
            subscriptions.insert(sub_list)
            return sub_list, 201
        else:
            response, error = self.check_filter(json_data, user_id)
            subscriptions.insert(response)
            return response, error

    def check_filter(self, bus_filter, user_id):
        result, errors = bus_filter_schema.load(bus_filter)
        if errors:
            return errors, 422

        user = users.get(user_id)
        if user:
            bus_filter_id = filters.search(result)

            if not bus_filter_id:
                bus_filter_id = filters.insert(result)['generated_keys'][0]

            subscription = {'user_id': user_id, 'filter_id': bus_filter_id}
            return subscription, None

        else:
            return {'message': 'User not found'}, 404
