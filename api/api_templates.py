from flask import Flask, Response
from flask_restful import Resource, request

from bussiness.users import UsersHandler
from bussiness.bus_filters import BusFiltersHandler
from bussiness.subscriptions import SubscriptionsHandler, SubscriptionSchema
from bussiness.templates import TemplatesHandler, TemplateSchema

import utils.json_parser as json_parser

users = UsersHandler()
filters = BusFiltersHandler()
subscriptions = SubscriptionsHandler()
templates = TemplatesHandler()
templates_schema = TemplateSchema()


class TemplatesView(Resource):
    """
    Templates endpoints /templates/
    """

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

        templates.insert(result)
        return result, 201


class TemplateView(Resource):
    """
    Template endpoints /templates/id
    """

    def get(self, template_id):
        """
        Get specific template
        """
        response = templates.get(template_id)
        
        if response:
            return response
        else:
            return {'message': 'Template not found'}, 404

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

        template = templates.get(template_id)
        if template:
            templates.edit(result, template_id)
            return result
        else:
            return {'message': 'Template not found'}, 404

    def delete(self, template_id):
        """
        Delete template by his id
        """
        template = templates.get(template_id)
        if template:
            templates.delete(template_id)
            response = {'deleted': True}
            return response
        else:
            return {'message': 'Template not found'}, 404
