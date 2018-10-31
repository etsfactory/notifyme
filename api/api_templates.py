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

from bussiness.templates import TemplatesHandler
from bussiness.templates import TemplateSchema
from bussiness.templates import Template

import utils.json_parser as json_parser

users = UsersHandler()
filters = BusFiltersHandler()
subscriptions = SubscriptionsHandler()
templates = TemplatesHandler()
templates_schema = TemplateSchema()

class TemplatesView(Resource):

    def get(self):
        """
        Get templates from the db
        """
        response = json_parser.to_json_list(templates.get())
        return response

    def post(self):
        """
        Create template
        """
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        result, errors = templates_schema.load(json_data)
        if errors:
            return errors, 422

        template = Template(result['name'], result['text'])
        templates.insert(template)
        response = json_parser.to_json_list(template)
        return response, 201
    
class TemplateView(Resource):

    def get(self, template_id):
        """
        Get specific template
        """
        template = templates.get(template_id)
        response = json_parser.to_json_list(template)
        return response
 
    def put(self, template_id):
        """
        Update template passing his id
        """
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        result, errors = templates_schema.load(json_data)
        if errors:
            return errors, 422

        template = Template(result['name'], result['text'])
        templates.edit(template, template_id)
        response = json_parser.to_json_list(template)
        return response

    def delete(self, subscription_id):
        """
        Delete template by his id
        """
        subscription = subscriptions.get(subscription_id)
        subscriptions.delete(subscription)
        response = json_parser.to_json_list(subscription)
        return response