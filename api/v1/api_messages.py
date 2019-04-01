"""
API messages handler
"""

from flask_restful import Resource, request

from bussiness.messages import MessagesHandler

messages = MessagesHandler()

class MessagesView(Resource):
    """
    Messages endpoints /messages/
    """

    @staticmethod
    def get():
        """
        Get templates from the db
        """
        response = messages.get()
        return response