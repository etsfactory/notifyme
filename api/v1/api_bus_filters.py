"""
APi bus filters handler
"""
from flask_restful import Resource, request, reqparse
from itertools import groupby

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

    @staticmethod
    def get():
        """
        Get bus filters from the db
        """
        group_by = request.args.get('group_by')
        bus_filters = filters.get()
        if group_by:
            modified_data = {}
            for entry in bus_filters:
                category = entry.get('category')
                if category:
                    try:
                        modified_data[category].append(entry)
                    except KeyError:
                        modified_data[category] = [entry]
                else:
                    return bus_filters
            return modified_data
        else:
            return bus_filters

    def post(self):
        """
        Create bus filter and store in the db
        """
        json_data = request.get_json(force=True)
        bus_filter_list = []
        if not json_data:
            return {'message': 'No input data provided'}, 400

        if isinstance(json_data, list):

            for bus_filter in json_data:
                response, http_code = self.check_bus_filter(bus_filter)

                if http_code != 201:
                    return response, http_code

                bus_filter_list.append(response)
            filters.insert(bus_filter_list)
            return bus_filter_list, 201

        response, http_code = self.check_bus_filter(json_data)
        if http_code != 201:
            return response, http_code

        filters.insert(response)
        return response, 201

    @staticmethod
    def check_bus_filter(bus_filter):
        """
        Check new bus filter with his schema.
        It returns result or error with his http code
        :bus_filter: Bus filter to check
        """
        result, errors = bus_filter_schema.load(bus_filter)
        if errors:
            return errors, 422

        return result, 201


class BusFilterView(Resource):
    """
    Specific bus filter endpoints /bus_filter/id
    """

    @staticmethod
    def get(bus_filter_id):
        """
        Get specific bus filter by his id
        """
        response = filters.get(bus_filter_id)

        if response:
            return response

        return {'message': 'Bus filter not found'}, 404

    @staticmethod
    def put(bus_filter_id):
        """
        Update bus filter passing his id
        """
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400
        result, errors = bus_filter_schema.load(json_data)

        if errors:
            return errors, 422

        bus_filter = filters.get(bus_filter_id)
        if bus_filter:
            filters.edit(result, bus_filter_id)
            return result

        return {'message': 'Bus filter not found'}, 404

    @staticmethod
    def delete(bus_filter_id):
        """
        Delete bus filter by his id
        """
        bus_filter = filters.get(bus_filter_id)

        if bus_filter:
            filters.delete(bus_filter_id)
            response = {'deleted': True}
            return response

        return {'message': 'Bus filter not found'}, 404


class BusFilterTemplateView(Resource):
    """
    Specific bus filter templates endpoints /bus_filter/id/templates
    """

    @staticmethod
    def get(bus_filter_id):
        """
        Get template from bus filter
        """
        bus_filter = filters.get(bus_filter_id)
        if bus_filter:
            template_id = bus_filter.get('template_id')
            if template_id:
                template = templates.get(bus_filter['template_id'])
                if template:
                    return template
            return []

        return {'message': 'Bus filter not found'}, 404

    @staticmethod
    def post(bus_filter_id):
        """
        Creates template for the bus filter passing his id
        """
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400
        result, errors = template_schema.load(json_data)

        if errors:
            return errors, 422

        bus_filter = filters.get(bus_filter_id)
        if bus_filter:
            template_id = templates.insert(result)[0]

            bus_filter['template_id'] = template_id
            filters.edit(bus_filter, bus_filter_id)

            return result

        return {'message': 'Bus filter not found'}, 404


class BusFilterUsersView(Resource):
    """
    Specific bus filter users endpoints /bus_filter/id/users
    """

    @staticmethod
    def get(bus_filter_id):
        """
        Get users from bus filter id
        """
        bus_filter = filters.get(bus_filter_id)

        if bus_filter:
            subs = subscriptions.get_users_by_filter(bus_filter)
            return subs

        return {'message': 'Bus filter not found'}, 404

    def post(self, bus_filter_id):
        """
        Add user to filter
        """
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400

        if isinstance(json_data, list):
            sub_list = []
            for user in json_data:
                response, error = self.check_user(
                    user, bus_filter_id)
                if error:
                    return response, error
                sub_list.append(response)
            subscriptions.insert(sub_list)
            return sub_list, 201

        response, error = self.check_user(
            json_data, bus_filter_id)
        subscriptions.insert(response)
        return response, error

    @staticmethod
    def check_user(user, bus_filter_id):
        """
        Check user provided with his schema. If no errors
        check if bus filter exits and insert new subscription.
        Returns the subscription created or the errors with the http code
        :user: Created user
        :bus_filter_id: Bus filter id to associate with the user
        """
        result, errors = user_schema.load(user)
        if errors:
            return errors, 422

        bus_filter = filters.get(bus_filter_id)
        if bus_filter:
            user_searched_id = users.search(result)
            if not user_searched_id:
                user_id = users.insert(result)[0]
            else:
                user_id = user_searched_id

            subscription = {'user_id': user_id, 'filter_id': bus_filter_id}
            return subscription, None

        return {'message': 'User not found'}, 404


class BusFilterUserView(Resource):
    def delete(self, bus_filter_id, user_id):
        """
        Delete bus filter from a user
        """
        bus_filter = filters.get(bus_filter_id)
        if bus_filter:
            sub_list = subscriptions.get()
            sub = [
                x for x in sub_list if (
                    x.get('user_id') == user_id and x.get('filter_id') == bus_filter_id)]
            if sub:
                subscriptions.delete(sub[0].get('id'))
                response = {'deleted': True}
                return response

        return {'message': 'Bus filter not found'}, 404
