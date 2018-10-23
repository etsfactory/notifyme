from flask import Flask, Response, jsonify
from flask_restful import Resource, Api, request
from marshmallow import pprint

from bussiness.bus_filters import BusFiltersHandler
from bussiness.bus_filters import BusFilter
from bussiness.bus_filters import BusFilterSchema

import utils.json_parser as json_parser

filters = BusFiltersHandler()
bus_filter_schema = BusFilterSchema()

class BusFilterView(Resource):

    def get(self, bus_filter_id):
        response = json_parser.to_json_list(filters.get()[int(bus_filter_id)])
        return jsonify(response)

    def put(self, bus_filter_id):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        result, errors = bus_filter_schema.load(json_data)
        if errors:
            return errors, 422
 
        bus_filter = BusFilter(result['exchange'], result['key'], result['id'])
        print(str(bus_filter.__dict__))
        filters.edit(bus_filter)
        return {'edited': True}

class BusFiltersView(Resource):
    def get(self):
        response = json_parser.to_json_list(filters.get())
        return jsonify(response)
   