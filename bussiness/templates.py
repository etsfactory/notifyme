
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
        :template_id: Template id to search for if provided
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
        :template: Template or template list to edit
        """
        result, errors = TemplateSchema().load(template)
        if errors:
            st.logger.error('Template creation error: %s', errors)
        else:
            return self.db_handler.insert_data(result)

    def edit(self, template, template_id):
        """
        Modify template by his id
        :template: Template modified
        :template_id: Template id to search for
        """
        self.db_handler.edit_data(template, template_id, 'id')

    def delete(self, template_id):
        """
        Delete template by his id
        :template_id: Template id to search for
        """
        self.db_handler.delete_data(template_id)

    def get_by_name(self, name):
        """
        Get template by his name
        :name: Name of the template to search
        """
        return self.db_handler.filter_data({'name': name})

    def search(self, template):
        """
        Search template with template provided. Return his id
        :template: Template without id to search.
        """
        templates = self.db_handler.filter_data(
            {'name': template.name, 'text': template.text})
        if len(templates) > 0:
            return templates[0]['id'], False
        else:
            return None, True

    def create_default(self):
        """
        Create and store default template
        """
        default_template = {'name': 'default',
                            'text': st.DEFAULT_TEMPLATE_TEXT, 'subject': st.DEFAULT_TEMPLATE_SUBJECT}
        return self.insert(default_template)['generated_keys'][0]

    def get_default_template(self):
        """
        Returns template. If no template is stored creates default one
        """
        default_template = self.get_by_name('default')
        if (len(default_template) > 0):
            return default_template[0]['id']
        else:
            return self.create_default()

    def parse(self, field, data):
        """
        Parse variables of the template. It searchs for the variables
        provided and replaces it with the data
        :field: Name of the field of the template. Subject or text
        :data: Dictionary of variables to replace. It searchs them in the template
        """
        if isinstance(data, dict):
            text = field
            for key in data:
                parse_regex = '\[\[' + key + '\]\]'
                text = re.sub(parse_regex, data[key], text)

                # If var has not been parsed, delete it

                delete_regex = '\[\[+.*?\]\]'
                text = re.sub(delete_regex, '', text)
            return str(text)
        else:
            return str(field)
