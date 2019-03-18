import re
from marshmallow import Schema, fields

import settings as st
import datetime


from bussiness.db_handler import DBHandler


class MessagesHandler():
    """
    Templates handlers class to get, edit,
    and streaming users from the database
    """

    def __init__(self):
        self.db_handler = DBHandler("messages")
        self.db_handler.create_table()

    def get(self, key=None):
        """
        Get all templates from the database
        :template_id: Template id to search for if provided
        """
        return self.db_handler.get_data(key)
    
    def insert(self, msgs):
        """
        Insert message to the database
        :message: message to insert
        """
        messages = self.get()
        for message in messages:
            if message['date'] < str(datetime.datetime.today().date()):
                self.delete(message.id)

        return self.db_handler.insert_data(msgs)

    def delete(self, message_id):
        """
        Delete message by his id
        :message_id: Message id to search for
        """
        self.db_handler.delete_data(message_id)