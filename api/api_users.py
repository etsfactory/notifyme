from flask import Flask, Response
from flask_restful import Resource, Api, request
from marshmallow import pprint

from bussiness.users import UsersHandler
from bussiness.users import User
from bussiness.users import UserSchema

from bussiness.subscriptions import SubscriptionsHandler
from bussiness.subscriptions import Subscription

from bussiness.bus_filters import BusFilterSchema
from bussiness.bus_filters import BusFilter
from bussiness.bus_filters import BusFiltersHandler

import utils.json_parser as json_parser

users = UsersHandler()
subscriptions = SubscriptionsHandler()
filters = BusFiltersHandler()
user_schema = UserSchema()
bus_filter_schema = BusFilterSchema()

class UsersView(Resource):
    """
    Handles users list endpoints
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
        if not json_data:
               return {'message': 'No input data provided'}, 400
        result, errors = user_schema.load(json_data)
        if errors:
            return errors, 422

        user = User(result['name'], result['email'])
        users.insert(user)
        response = json_parser.to_json_list(user)
        return response, 201


class UserView(Resource):
    """
    Handles user endpoints
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

        user = User(result['name'], result['email'])
        users.edit(user, user_id)
        response = json_parser.to_json_list(user)
        return response

    def delete(self, user_id):
        """
        Delete user from the db passing an user id
        """
        user = users.get(user_id)
        users.delete(user)
        response = json_parser.to_json_list(user)
        return response

class UserFiltersView(Resource):
    """
    Handles user bus filter endpoints
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

        bus_filter = BusFilter(result['exchange'], result['key'])
        bus_filter_id, not_exits = filters.search(bus_filter)

        if not_exits:
            bus_filter_id = filters.insert(bus_filter)['generated_keys'][0]

        subscription = Subscription(user_id, bus_filter_id)
        print(str(subscription.__dict__))
        subscriptions.insert(subscription)

        response = json_parser.to_json_list(subscription)
        return response

   