# -*- coding: utf-8 -*-
"""
Rethink connector to a rethink database
"""
import rethinkdb as r
from exceptions.db_exceptions import WriteError, ReadError, ConnectionLost


class RethinkHandler(object):
    """
    Rethink handler to handle connection with database
    """

    def __init__(self, server, port, db_name, user=None, password=None):
        self.db_name = db_name
        try:
            self.con = r.connect(
                host=server,
                port=port,
                db=db_name,
                user=user,
                password=password).repl()
        except BaseException:
            raise ConnectionLost()

        self.create_database()

    def create_database(self):
        """
        Database creation.
        """
        db_name = self.db_name
        con = self.con
        if db_name not in r.db_list().run(con):
            r.db_create(db_name).run(con)

    def reset_database(self):
        """
        Database reset. If the database exists drops it and recreates.
        If it doesn't exist, create it
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
        if table_name not in r.db(db_name).table_list().run(con):
            r.db(db_name).table_create(table_name, primary_key=key).run(con)

    def insert_data(self, table_name, data):
        """
        Insert data into table
        """
        db_name = self.db_name
        con = self.con
        try:
            if table_name in r.db(db_name).table_list().run(con):
                return r.table(table_name).insert(data).run(con)
        except BaseException:
            raise WriteError()

    def get_data(self, table_name, key):
        """"
        Returns data from table
        """
        con = self.con
        try:
            if key:
                return r.table(table_name).get(key).run(con)
            return r.table(table_name).run(con)

        except BaseException:
            raise ReadError()

    def edit_data(self, table_name, primary_key, new_data):
        """
        Edit document from database with a primary key
        """
        con = self.con
        try:
            return r.table(table_name).get(
                primary_key).update(new_data).run(con)

        except BaseException:
            raise WriteError()

    def filter_data(self, table_name, filter_data):
        """
        Returns filtered documents from database.
        :filter_data: Object with a key and his value
        """
        con = self.con
        try:
            return r.table(table_name).filter(filter_data).run(con)
        except BaseException:
            raise ReadError()

    def delete_data(self, table_name, data_to_delete):
        """
        Delete documents from database
        :filter_data: Object with a key and his value
        """
        con = self.con
        try:
            return (r.table(table_name).get(data_to_delete).delete().run(con))
        except BaseException:
            raise ReadError()

    def join_tables(self, table1, table2, table3, key1, key2):
        con = self.con
        try:
            return r.table(table1).eq_join(key1, r.table(table2)).without({"right": {"id": True}}).zip(
            ).eq_join(key2, r.table(table3)).without({"right": {"id": True}}).zip().run(con)

        except BaseException:
            raise ReadError()
