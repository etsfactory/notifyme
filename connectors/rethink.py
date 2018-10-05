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
