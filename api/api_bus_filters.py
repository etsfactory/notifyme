from flask import Flask, Response
from flask_restful import Resource, Api, request
from marshmallow import pprint

from bussiness.bus_filters import BusFiltersHandler
from bussiness.bus_filters import BusFilter
from bussiness.bus_filters import BusFilterSchema
from bussiness.subscriptions import SubscriptionsHandler

import utils.json_parser as json_parser

filters = BusFiltersHandler()
subscriptions = SubscriptionsHandler()
bus_filter_schema = BusFilterSchema()

class BusFiltersView(Resource):
    def get(self):
        response = json_parser.to_json_list(filters.get())
        return response
        
    def post(self):
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
        response = json_parser.to_json_list(filters.get()[int(bus_filter_id)])
        return response

    def put(self, bus_filter_id):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        result, errors = bus_filter_schema.load(json_data)
        if errors:
            return errors, 422
 
        bus_filter = BusFilter(result['exchange'], result['key'], result['id'])
        filters.edit(bus_filter)
        response = json_parser.to_json_list(bus_filter)
        return response

class BudFilterUsersView(Resource):
    def get(self, bus_filter_id):
        bus_filter = filters.get()[int(bus_filter_id)]
        subs = subscriptions.get_users_by_filter(bus_filter)
        response = json_parser.to_json_list(subs)
        return response
