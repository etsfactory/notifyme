# -*- coding: utf-8 -*-
import rethinkdb as r

class RethinkHandler(object): 
    def __init__(self, server, port, db_name):
        self.db_name = db_name
        self.con = r.connect(host=server, port=port,
                   db=db_name)
        self.create_database()

    def create_database(self):
        db_name = self.db_name
        con = self.con
        try:
            r.db_create(db_name).run(con)
        except: 
            r.db_drop(db_name).run(con)
            r.db_create(db_name).run(con)
    
    def insert_data(self, table_name, data):
        db_name = self.db_name
        con = self.con
        try:
            r.db(db_name).table_drop(table_name).run(con)            
        except:
            r.db(db_name).table_create(table_name).run(con)
            r.table(table_name).insert(data).run(con)

    def get_data(self, table_name):
        con = self.con
        try:
            return r.table(table_name).changes().run(con)
        except: 
            'Error reading database'