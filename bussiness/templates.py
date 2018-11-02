
"""
Templates handler
"""
import re
import settings as st

from connectors.rethink import RethinkHandler
from bussiness.db_handler import DBHandler
from marshmallow import Schema, fields, pprint

class TemplateSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    text = fields.Str()
    subject = fields.Str()

class Template(object):
    def __init__(self, name, text, subject=None, id=None):
        self.name = name
        self.text = text
        self.subject = subject
        if id:
            self.id = id
    
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
        return self.to_object(self.db_handler.get_data(template_id))

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
        return self.db_handler.insert_data(template)

    def edit(self, template, template_id):
        """
        Modify template by his id
        """
        self.db_handler.edit_data(template, template_id, 'id')
    
    def delete(self, template):
        self.db_handler.delete_data(template.id)
    
    def search(self, template):
        templates = self.db_handler.filter_data({'name': template.name, 'text': template.text})
        if len(templates) > 0:
            return templates[0]['id'], False
        else:
            return None, True
    
    def create_default(self):
        default_template = Template(st.DEFAULT_TEMPLATE_NAME, st.DEFAULT_TEMPLATE_TEXT, st.DEFAULT_TEMPLATE_SUBJECT)
        self.default_template_id = self.insert(default_template)['generated_keys'][0]
    
    def parse(self, field, data):
        if isinstance(data, dict):
            text = field
            for key in data:
                regex = '\[\[' + key + '\]\]'
                text = re.sub(regex, data[key], text)
            return str(text)
        else:
            return str(field)
     
    def to_object(self, data):
        """
        Parse db template object to Template instance
        """
        if (not data):
            return None
        templates = []
        if isinstance(data, dict):
            return Template(data['name'], data['text'], data['subject'], data['id'])
        else:
            for template in data:
                templates.append(Template(template['name'], template['text'], template['subject'], template['id']))
            return templates
    