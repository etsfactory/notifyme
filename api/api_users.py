from flask import Flask, Response
from flask_restful import Resource, Api, request
from marshmallow import pprint

from bussiness.users import UsersHandler
from bussiness.subscriptions import SubscriptionsHandler
from bussiness.users import User
from bussiness.users import UserSchema

import utils.json_parser as json_parser

users = UsersHandler()
subscriptions = SubscriptionsHandler()
user_schema = UserSchema()

class UsersView(Resource):

    def get(self):
        response = json_parser.to_json_list(users.get())
        return response

    def post(self):
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

    def get(self, user_id):
        response = json_parser.to_json_list(users.get()[int(user_id)])
        return response

    def put(self, user_id):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        result, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
 
        user = User(result['name'], result['email'], result['id'])
        users.edit(user)
        response = json_parser.to_json_list(user)
        return response

class UserFiltersView(Resource):

    def get(self, user_id):
        user = users.get()[int(user_id)]
        subs = subscriptions.get_filters_by_user(user)
        response = json_parser.to_json_list(subs)
        return response
    

   