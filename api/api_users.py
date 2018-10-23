from flask import Flask, Response, jsonify
from flask_restful import Resource, Api, request
from marshmallow import pprint

from bussiness.users import UsersHandler
from bussiness.users import User
from bussiness.users import UserSchema

import utils.json_parser as json_parser

users = UsersHandler()
user_schema = UserSchema()

class UserView(Resource):

    def get(self, user_id):
        response = json_parser.to_json_list(users.get()[int(user_id)])
        return jsonify(response)

    def put(self, user_id):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        result, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
 
        user = User(result['name'], result['email'], result['id'])
        print(str(user.__dict__))
        users.edit(user)
        return {'edited': True}

class UsersView(Resource):
    def get(self):
        response = json_parser.to_json_list(users.get())
        return jsonify(response)
   