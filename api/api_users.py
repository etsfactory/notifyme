"""
API users handler
"""
from flask_restful import Resource, request

from bussiness.users import UsersHandler, UserSchema
from bussiness.subscriptions import SubscriptionsHandler
from bussiness.bus_filters import BusFiltersHandler, BusFilterSchema


users = UsersHandler()
subscriptions = SubscriptionsHandler()
filters = BusFiltersHandler()
user_schema = UserSchema()
bus_filter_schema = BusFilterSchema()


class UsersView(Resource):
    """
    Handles users list endpoints /users/
    """

    @staticmethod
    def get():
        """
        Get users from the db
        """
        response = users.get()
        return response

    def post(self):
        """
        Create user and stores in the db
        """
        json_data = request.get_json(force=True)
        users_list = []
        if not json_data:
            return {'message': 'No input data provided'}, 400

        if isinstance(json_data, list):

            for user in json_data:
                response, http_code = self.check_user(user)

                if http_code != 201:
                    return response, http_code

                users_list.append(response)
            users.insert(users_list)
            return users_list, 201

        response, http_code = self.check_user(json_data)
        if http_code != 201:
            return response, http_code

        users.insert(response)
        return response, 201

    @staticmethod
    def check_user(user):
        """"
        Compare user with his schema,
        return result or errors with http code
        """
        result, errors = user_schema.load(user)
        if errors:
            return errors, 422

        return result, 201


class UserView(Resource):
    """
    Specific user endpoints /users/id
    """

    @staticmethod
    def get(user_id):
        """
        Get specific user from the db
        """

        response = users.get(user_id)

        if response:
            return response

        return {'message': 'User not found'}, 404

    @staticmethod
    def put(user_id):
        """
        Update user passing an id
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        result, errors = user_schema.load(json_data)
        if errors:
            return errors, 422

        user = users.get(user_id)
        if user:
            users.edit(result, user_id)
            return result

        return {'message': 'User not found'}, 404

    @staticmethod
    def delete(user_id):
        """
        Delete user from the db passing an user id
        """
        user = users.get(user_id)
        if user:
            users.delete(user_id)
            subscriptions.delete_user(user_id)
            response = {'deleted': True}
            return response

        return {'message': 'User not found'}, 404


class UserFiltersView(Resource):
    """
    Specific user bus filters /users/id/bus_filters
    """

    @staticmethod
    def get(user_id):
        """
        Get user bus filters
        """
        user = users.get(user_id)
        if user:
            response = subscriptions.get_filters_by_user(user)
            return response

        return {'message': 'User not found'}, 404

    def post(self, user_id):
        """
        Add bus filter to an user
        """
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400

        if isinstance(json_data, list):
            sub_list = []
            for bus_filter in json_data:
                response, error = self.check_filter(bus_filter, user_id)
                if error:
                    return response, error
                sub_list.append(response)
            subscriptions.insert(sub_list)
            return sub_list, 201

        response, error = self.check_filter(json_data, user_id)
        if error:
            return response, error
        subscriptions.insert(response)
        return response, error

    @staticmethod
    def check_filter(bus_filter, user_id):
        """
        Return created subscription by passing user id
        Checks if the bus filter exists, if not, insert
        into database and return his id
        """
        result, errors = bus_filter_schema.load(bus_filter)
        if errors:
            return errors, 422

        user = users.get(user_id)
        if user:
            key = result.get('key')
            searched_bus_filter = filters.get_by_exchange_key(
                result['exchange'], key)

            if not searched_bus_filter:
                bus_filter_id = filters.insert(result)[0]
            else:
                bus_filter_id = searched_bus_filter['id']

            subscription = {'user_id': user_id, 'filter_id': bus_filter_id}
            return subscription, None

        return {'message': 'User not found'}, 404


class UserFilterView(Resource):
    def delete(self, user_id, bus_filter_id):
        """
        Delete bus filter from a user
        """
        user = users.get(user_id)
        if user:
            sub_list = subscriptions.get()
            print(sub_list)
            sub = [
                x for x in sub_list if (
                    x.get('user_id') == user_id and x.get('filter_id') == bus_filter_id)]
            if sub:
                subscriptions.delete(sub[0].get('id'))
                response = {'deleted': True}
                return response

        return {'message': 'User not found'}, 404
