# -*- coding: utf-8 -*-
import rethinkdb as r

class RethinkHandler(object): 
    def __init__(self, server, port, db_name):
        self.db_name = db_name
        self.con = r.connect(host=server, port=port,
                   db=db_name)
        self.create_database()
       
    def create_database(self):
        """
        Database creation. If the database exists drops it and recreates
        """
        db_name = self.db_name
        con = self.con
        if db_name in r.db_list().run(con):
            r.db_drop(db_name).run(con)
        r.db_create(db_name).run(con)
    
    def create_table(self, table_name):
        """
        Table creation. If the Table exists drops it and recreates
        """
        db_name = self.db_name
        con = self.con   
        if table_name in r.db(db_name).table_list().run(con):
            r.db(db_name).table_drop(table_name).run(con)            
        r.db(db_name).table_create(table_name).run(con)
    
    def insert_data(self, table_name, data):
        """
        Insert data into table
        """
        con = self.con        
        r.table(table_name).insert(data).run(con)

  