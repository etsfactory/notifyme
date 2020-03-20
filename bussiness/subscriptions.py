
"""
Users handler
"""
from marshmallow import Schema, fields

from bussiness.db_handler import DBHandler
from bussiness.users import UsersHandler
from bussiness.bus_filters import BusFiltersHandler
from bussiness.templates import TemplatesHandler


class SubscriptionSchema(Schema):
    """
    Subscription schema to validate subscriptions
    """
    id = fields.Str()
    user_id = fields.Str(required=True)
    filter_id = fields.Str(required=True)
    template_id = fields.Str()


class SubscriptionsHandler():
    """
    Subscription type handlers class to get, edit, and streaming
    subscriptions from the database
    """

    def __init__(self):
        self.db_handler = DBHandler('subscriptions')
        self.db_handler.create_table('id')
        self.users = UsersHandler()
        self.filters = BusFiltersHandler()
        self.templates = TemplatesHandler()

    def get(self, sub_id=None):
        """
        Get all the subscriptions from the database.
        If id is provided search for a single subscription
        :sub_id: Id of the subscription to search for if provided
        """
        return self.db_handler.get_data(sub_id)

    def get_with_relationships(self):
        """
        Get subscriptions joining users and bus_filtes tables
        """
        sub_list = []
        subscriptions = self.db_handler.join_tables(
            "subscriptions",
            "users",
            "bus_filters",
            "user_id",
            "filter_id")
        for sub in subscriptions:
            sub_list.append(sub)
        return sub_list

    def get_realtime(self):
        """
        Get all subscriptions from the database in realtime.
        If user is edited in the db it returns the change.
        This method blocks the current thread
        use this method in a separated thread
        """
        return self.db_handler.get_data_streaming()

    def get_users_by_filter(self, bus_filter):
        """
        Get user associates with filter
        :bus_filter: Bus filter to search users
        """
        users = []
        subscriptions = self.get_by_filter(bus_filter)
        for subscription in subscriptions:
            user = self.users.get(subscription['user_id'])
            users.append(user)
        return users

    def get_filters_by_user(self, user):
        """
        Get filters associates with user
        :user: User to seach for bus filters
        """
        filters = []
        subscriptions = self.get_by_user(user)
        for subscription in subscriptions:
            bus_filter = self.filters.get(subscription['filter_id'])
            filters.append(bus_filter)
        return filters

    def get_filters_by_template(self, template):
        """
        Get bus filters assigned to a template
        :template: Template to search for his filters
        """
        filters = []
        subscriptions = self.get_by_template(template)
        for subscription in subscriptions:
            template = self.templates.get(subscription['template_id'])
            filters.append(template)
        return filters

    def get_by_id(self, subsc_id):
        """
        Get subscription by his id
        :subsc_id: ID of the subscription to search
        """
        return self.db_handler.filter_data({'id': subsc_id})

    def get_by_template(self, template):
        """
        Get subscription searching by his template
        :template: Template to search for
        """
        return self.db_handler.filter_data({'template_id': template['id']})

    def get_by_filter(self, bus_filter):
        """
        Get subscription by his id
        :bus_filter: Bus filter to search for
        """
        return self.db_handler.filter_data({'filter_id': bus_filter['id']})

    def get_by_filter_id(self, bus_filter_id):
        """
        Get subscription by his id
        :bus_filter: Bus filter to search for
        """
        return self.db_handler.filter_data({'filter_id': bus_filter_id})

    def get_by_user(self, user):
        """
        Get subscription by his id
        :user: User to seach for
        """
        return self.db_handler.filter_data({'user_id': user['id']})

    def insert(self, subscriptions):
        """
        Insert subscriptions to the database
        :subscriptions: Subscription or bus subscriptions to insert
        """
        if isinstance(subscriptions, list):
            for sub in subscriptions:
                if not sub.get('template_id'):
                    sub = self.set_subscription_template(sub)
        else:
            if not subscriptions.get('template_id'):
                subscriptions = self.set_subscription_template(subscriptions)
        return self.db_handler.insert_data(subscriptions)

    def set_subscription_template(self, subscription):
        """
        Sets subscription notification template
        If the bus filter associated with the subscription
        has template uses it. If not create default one
        :subscription: Subscription to add template
        """
        bus_filter = self.filters.get(subscription.get('filter_id'))
        template_id = ''
        if bus_filter:
            if isinstance(bus_filter, list):
                bus_filter = bus_filter[0]
            template_id = bus_filter.get('template_id')
        if not hasattr(
                subscription,
                'template_id') and template_id and bus_filter:
            subscription['template_id'] = bus_filter['template_id']
        else:
            subscription['template_id'] = self.templates.get_default_template()
        return subscription

    def edit(self, subscription, subscription_id):
        """
        Modify subscriptions
        :subscription: Modified subscription
        :subscription_id: Id of the subscription to edit
        """
        self.db_handler.edit_data(subscription, subscription_id)

    def delete_user(self, user_id):
        """
        Delete subscriptions associated with the user
        :user_id: user id to search for
        """
        subscriptions = self.get()
        for sub in subscriptions:
            if sub['user_id'] == user_id:
                self.delete(sub['id'])

    def delete_bus_filter(self, bus_filter):
        """
        Delete subscriptions associated with the bus filter
        :bus_filter_id: filter id to search for
        """
        subscriptions = self.db_handler.filter_data(
            {'filter_id': bus_filter['id']})
        for sub in subscriptions:
            self.delete(sub['id'])

    def edit_subscriptions_template(self, bus_filter):
        subscriptions = self.db_handler.filter_data({'filter_id': bus_filter.get('id')})
        for subs in subscriptions:
            subs['template_id'] = bus_filter.get('template_id')
            print(subs)
            self.edit(subs, subs['id'])


    def subscriptions_template(self, template_id):
        """
        Return subscriptions with specific template id
        """
        return self.db_handler.filter_data({'template_id': template_id})

    def delete(self, subscription_id):
        """
        Delete subscription.
        :subscription_id: Subscription id to delete
        """
        self.db_handler.delete_data(subscription_id)
