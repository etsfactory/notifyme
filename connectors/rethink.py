# -*- coding: utf-8 -*-
"""
Rethink connector to a rethink database
"""
import time
import rethinkdb as r
from exceptions.db_exceptions import WriteError, ReadError, ConnectionLost


class RethinkHandler():
    """
    Rethink handler to handle connection with database
    """

    def __init__(self, server, port, db_name, user=None, password=None):
        self.server = server
        self.port = port
        self.db_name = db_name
        self.user = user
        self.password = password

        self.wait_time = 100
        self.n_retries = 2

        self.con = self.connect()
        self.create_database()
    
    def connect(self):
        """
        Connect to the database
        """
        try:
            return r.connect(
                host=self.server,
                port=self.port,
                db=self.db_name,
                user=self.user,
                password=self.password).repl()
        except ConnectionLost:
            self.reconnect()
            raise ConnectionLost()
    
    def reconnect(self):
        self.con.reconnect(noreply_wait=False)

    def create_database(self):
        """
        Database creation.
        """
        db_name = self.db_name
        with self.connect() as conn:
            if db_name not in r.db_list().run(conn):
                r.db_create(db_name).run(conn)

    def reset_database(self):
        """
        Database reset. If the database exists drops it and recreates.
        If it doesn't exist, create it
        """
        db_name = self.db_name
        with self.connect() as conn:
            if db_name in r.db_list().run(conn):
                r.db_drop(db_name).run(conn)
                r.db_create(db_name).run(conn)

    def create_table(self, table_name, key='id'):
        """
        Table creation. If the Table exists drops it and recreates
        """
        db_name = self.db_name
        with self.connect() as conn:
            if table_name not in r.db(db_name).table_list().run(conn):
                r.db(db_name).table_create(table_name, primary_key=key).run(conn)

    def insert_data(self, table_name, data):
        """
        Insert data into table. The connection will be automatically closed 
        when execution reaches the end of the block 
        """
        db_name = self.db_name
        with self.connect() as conn:
            try:
                if table_name in r.db(db_name).table_list().run(conn):
                    return r.table(table_name).insert(data).run(conn)
            except BaseException:
                raise WriteError()

    def get_data(self, table_name, key):
        """"
        Returns data from table. The connection will be automatically closed 
        when execution reaches the end of the block 
        """
        with self.connect() as conn:
            try:
                if key:
                    return r.table(table_name).get(key).run(conn)
                return r.table(table_name).run(conn, time_format="raw")

            except BaseException:
                raise ReadError()

    def edit_data(self, table_name, primary_key, new_data):
        """
        Edit document from database with a primary key
        """
        with self.connect() as conn:
            try:
                return r.table(table_name).get(
                    primary_key).update(new_data).run(conn)

            except BaseException:
                raise WriteError()

    def replace_data(self, table_name, new_data, primary_key):
        """
        Edit document from database with a primary key
        """
        with self.connect() as conn:
            try:
                return (r.table(table_name).get(
                    primary_key).replace(new_data).run(conn))

            except BaseException:
                raise WriteError()

    def filter_data(self, table_name, filter_data):
        """
        Returns filtered documents from database.
        :filter_data: Object with a key and his value
        """
        with self.connect() as conn:
            try:
                return r.table(table_name).filter(filter_data).run(conn)
            except BaseException:
                raise ReadError()

    def delete_data(self, table_name, data_to_delete):
        """
        Delete documents from database
        :filter_data: Object with a key and his value
        """
        with self.connect() as conn:
            try:
                return r.table(table_name).get(data_to_delete).delete().run(conn)
            except BaseException:
                raise ReadError()

    def join_tables(self, table1, table2, table3, key1, key2):
        """
        Merge two tables
        :table1: Table in which the other tables are to be combined
        :table2: First table to merge (left table)
        :table3: Second table to merge (right table)
        :key1: Key to search in the left table
        :key2: KEy to search in the right table
        """
        with self.connect() as conn:
            try:
                return r.table(table1).eq_join(key1, r.table(table2)).without(
                    {"right": {"id": True}}).zip().eq_join(
                        key2, r.table(table3)).without(
                            {"right": {"id": True}}).zip().run(conn)

            except BaseException:
                raise ReadError()
