from flask import Flask, Response
from flask_restful import Resource, request

from bussiness.bus_filters import BusFiltersHandler, BusFilterSchema
from bussiness.users import UsersHandler, UserSchema
from bussiness.subscriptions import SubscriptionsHandler
from bussiness.templates import TemplatesHandler, TemplateSchema

filters = BusFiltersHandler()
subscriptions = SubscriptionsHandler()
bus_filter_schema = BusFilterSchema()
user_schema = UserSchema()
users = UsersHandler()
templates = TemplatesHandler()
template_schema = TemplateSchema()


class BusFiltersView(Resource):
    """
    Bus filters endpoint /bus_filters/
    """
    def get(self):
        """
        Get bus filters from the db
        """
        response = filters.get()
        return response

    def post(self):
        """
        Create bus filter and stores in the db
        """
        json_data = request.get_json(force=True)
        bus_filters = []

        if isinstance(json_data, list):
            for bus_filter in json_data:
                response, http_code = self.insert_bus_filter(bus_filter)
                bus_filters.append(bus_filter)

                if http_code == 422:
                    return response, 422

            return bus_filters, 201
        else:
            response, http_code = self.insert_bus_filter(json_data)
            return response, http_code

    def insert_bus_filter(self, data):
        """
        Validate bus filter and insert it into the database
        """
        result, errors = bus_filter_schema.load(data)
        if errors:
            return errors, 422

        filters.insert(result)
        return data, 201


class BusFilterView(Resource):
    """
    Specific bus filter endpoints /bus_filter/id
    """

    def get(self, bus_filter_id):
        """
        Get specific bus filter by his id
        """
        response = filters.get(bus_filter_id)
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

        filters.edit(result, bus_filter_id)
        return result

    def delete(self, bus_filter_id):
        """
        Delete bus filter by his id
        """
        filters.delete(bus_filter_id)
        response = {'deleted': True}
        return response


class BusFilterTemplateView(Resource):
    """
    Specific bus filter templates endpoints /bus_filter/id/templates
    """
    def get(self, bus_filter_id):
        """
        Get template from bus filter
        """
        bus_filter = filters.get(bus_filter_id)
        template = templates.get(bus_filter['template_id'])
        if template:
            return template
        else:
            return {'message': 'Bus filter does not have template'}, 404

    def post(self, bus_filter_id):
        """
        Creates template for the bus_filter
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        result, errors = template_schema.load(json_data)
        if errors:
            return errors, 422

        bus_filter = filters.get(bus_filter_id)

        template = {'name': result['name'], 'text': result['text']}
        template_id = templates.insert(template)['generated_keys'][0]

        bus_filter['template_id'] = template_id
        filters.edit(bus_filter, bus_filter_id)

        return template


class BusFilterUsersView(Resource):
    """
    Specific bus filter users endpoints /bus_filter/id/users
    """
    def get(self, bus_filter_id):
        """
        Get users from bus filter id
        """
        bus_filter = filters.get(bus_filter_id)
        subs = subscriptions.get_users_by_filter(bus_filter)
        return subs

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

        user_id, not_exits = users.search(result)
        if not_exits:
            user_id = users.insert(result)['generated_keys'][0]

        subscription = {'user_id': user_id, 'filter_id': bus_filter_id}
        subscriptions.insert(subscription)

        return subscription
