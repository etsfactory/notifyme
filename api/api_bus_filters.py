from flask import Flask, Response
from flask_restful import Resource, Api, request
from marshmallow import pprint

from bussiness.bus_filters import BusFiltersHandler
from bussiness.bus_filters import BusFilter
from bussiness.bus_filters import BusFilterSchema

from bussiness.users import UsersHandler
from bussiness.users import User
from bussiness.users import UserSchema

from bussiness.subscriptions import Subscription
from bussiness.subscriptions import SubscriptionsHandler

import utils.json_parser as json_parser

filters = BusFiltersHandler()
subscriptions = SubscriptionsHandler()
bus_filter_schema = BusFilterSchema()
user_schema = UserSchema()
users = UsersHandler()

class BusFiltersView(Resource):
    def get(self):
        """
        Get bus filters from the db
        """
        response = json_parser.to_json_list(filters.get())
        return response

    def post(self):
        """
        Create bus filter and stores in the db
        """
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        result, errors = bus_filter_schema.load(json_data)
        if errors:
            return errors, 422

        bus_filter = BusFilter(result['exchange'], result['key'])
        filters.insert(bus_filter)
        response = json_parser.to_json_list(bus_filter)
        return response, 201

class BusFilterView(Resource):

    def get(self, bus_filter_id):
        """
        Get specific bus filter by his id
        """
        response = json_parser.to_json_list(filters.get(bus_filter_id))
        return response

    def put(self, bus_filter_id):
        """
        Update bus filter passing his id
        """
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        result, errors = bus_filter_schema.load(json_data)
        if errors:
            return errors, 422

        bus_filter = BusFilter(result['exchange'], result['key'], result['id'])
        filters.edit(bus_filter, bus_filter_id)
        response = json_parser.to_json_list(bus_filter)
        return response

    def delete(self, bus_filter_id):
        """
        Delete bus filter by his id
        """
        bus_filter = filters.get(bus_filter_id)
        filters.delete(bus_filter)
        response = json_parser.to_json_list(bus_filter)
        return response

class BusFilterUsersView(Resource):

    def get(self, bus_filter_id):
        """
        Get users from bus filter id
        """
        bus_filter = filters.get(bus_filter_id)
        subs = subscriptions.get_users_by_filter(bus_filter)
        response = json_parser.to_json_list(subs)
        return response

    def post(self, bus_filter_id):
        """
        Add user to filter
        """
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        result, errors = user_schema.load(json_data)
        if errors:
            return errors, 422

        user = User(result['name'], result['email'])
        user_id, not_exits = users.search(user)
        if not_exits:
            user_id = users.insert(user)['generated_keys'][0]

        subscription = Subscription(user_id, bus_filter_id)
        # print(str(subscription.__dict__))
        subscriptions.insert(subscription)

        response = json_parser.to_json_list(subscription)
        return response
