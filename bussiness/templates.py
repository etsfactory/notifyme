
"""
Templates handler
"""
import re
import settings as st

from bussiness.db_handler import DBHandler
from marshmallow import Schema, fields

import utils.json_parser as json_parser


class TemplateSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True)
    text = fields.Str(required=True)
    subject = fields.Str()


class TemplatesHandler(object):
    """
    Templates handlers class to get, edit, and streaming users from the database
    """

    def __init__(self):
        self.db_handler = DBHandler("templates")
        self.db_handler.create_table()
        self.default_template_id = ''

    def get(self, template_id=None):
        """
        Get all templates from the database
        """
        return self.db_handler.get_data(template_id)

    def get_realtime(self):
        """
        Get all templates from the database in realtime.
        If template is added or modified in the db it returns the change.
        This method blocks the current thread so use this method in a separated thread
        """
        return self.db_handler.get_data_streaming()

    def insert(self, template):
        """
        Insert templates to the database
        """
        result, errors = TemplateSchema().load(json_parser.to_json_list(template))
        if errors:
            st.logger.error('Template creation error: %s', errors)
        else:
            return self.db_handler.insert_data(result)

    def edit(self, template, template_id):
        """
        Modify template by his id
        """
        self.db_handler.edit_data(template, template_id, 'id')

    def delete(self, template_id):
        self.db_handler.delete_data(template_id)

    def search(self, template):
        templates = self.db_handler.filter_data(
            {'name': template.name, 'text': template.text})
        if len(templates) > 0:
            return templates[0]['id'], False
        else:
            return None, True

    def create_default(self):
        default_template = {'name': st.DEFAULT_TEMPLATE_NAME,
                            'text': st.DEFAULT_TEMPLATE_TEXT, 'subject': st.DEFAULT_TEMPLATE_SUBJECT}
        self.default_template_id = self.insert(default_template)[
            'generated_keys'][0]

    def parse(self, field, data):
        if isinstance(data, dict):
            text = field
            for key in data:
                regex = '\[\[' + key + '\]\]'
                text = re.sub(regex, data[key], text)
            return str(text)
        else:
            return str(field)
