# -*- coding: utf-8 -*-
"""
Rethink connector to a rethink database
"""
import rethinkdb as r

class RethinkHandler(object):
    """
    Rethink handler to handle connection with database
    """
    def __init__(self, server, port, db_name):
        self.db_name = db_name
        self.con = r.connect(host=server, port=port,
                             db=db_name).repl()
        # self.create_database()

    def create_database(self):
        """
        Database creation. If the database exists drops it and recreates
        """
        db_name = self.db_name
        con = self.con
        if db_name in r.db_list().run(con):
            r.db_drop(db_name).run(con)
        r.db_create(db_name).run(con)

    def create_table(self, table_name, key='id'):
        """
        Table creation. If the Table exists drops it and recreates
        """
        db_name = self.db_name
        con = self.con
        if table_name in r.db(db_name).table_list().run(con):
            r.db(db_name).table_drop(table_name).run(con)
        r.db(db_name).table_create(table_name, primary_key=key).run(con)

    def insert_data(self, table_name, data):
        """
        Insert data into table
        """
        db_name = self.db_name
        con = self.con
        if table_name in r.db(db_name).table_list().run(con):
            return r.table(table_name).insert(data).run(con)

    def get_data(self, table_name):
        """"
        Returns data from table
        """
        con = self.con
        try:
            return r.table(table_name).run(con)
        except:
            print 'Error reading database'

    def edit_data(self, table_name, primary_key, new_data):
        """
        Edit document from database with a primary key
        """
        con = self.con
        try:
            return r.table(table_name).get(primary_key).update(new_data).run(con)
        except:
            print 'Error editing data'

    def filter_data(self, table_name, filter):
        """
        Returns filtered documents from database
        """
        con = self.con
        try:
            return r.table(table_name).filter(filter).run(con)
        except:
            print 'Error filtering data'

    def join_tables(self, table1, table2, table3, key1, key2):
        con = self.con
        return r.table(table1).eq_join(key1, r.table(table2)).zip().eq_join(key2, r.table(table3)).zip().run(con)
    
