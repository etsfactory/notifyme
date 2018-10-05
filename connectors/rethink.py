import rethinkdb as r

class RethinkHandler(object): 
    def __main__(self):
        r.connect( "172.17.0.3", 28015).repl()
