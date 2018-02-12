import MySQLdb as sql

from dbobjects import *
from config import *

class Reader(object):
    
    def __init__(self, connection):
        self.connection = connection
    
    def _select_query(self):
        pass

    def _update_query(self):
        pass
