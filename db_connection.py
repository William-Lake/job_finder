"""
DB Connection

Represents the connection to the database, 
centralizing transactions and management.
"""

import sqlite3
import os

class db_connection(object):

    def __init__(self):
        """Constructor"""

        current_dir = os.path.dirname(os.path.abspath(__file__))

        self.conn = sqlite3.connect(os.path.join(current_dir,'Helena_Jobs.db'))

    def execute_insert(self,statement,params=None):
        """Executes an INSERT on the database.
        
        Arguments:
            statement {str} -- The SQL statement to execute.
        
        Keyword Arguments:
            params {list} -- The parameters to use when executing the SQL statement. (default: {None})
        """

        if params == None: self.conn.execute(statement)
        
        else: self.conn.execute(statement,params)

    def execute_select(self,statement,params=None):
        """Executes a SELECT statement on the database, returning the results.
        
        Arguments:
            statement {str} -- The SQL statement to execute.
        
        Keyword Arguments:
            params {list} -- The parameters to use when executing the SQL statement. (default: {None})
        
        Returns:
            list -- The results of the given SQL SELECT statement.
        """

        if params == None: results = self.conn.execute(statement)

        else: results = self.conn.execute(statement,params)

        return results

    def execute_delete(self,statement,params=None):
        """Executes a DELETE statement on the database.
        
        Arguments:
            statement {str} -- The SQL statement to execute.
        
        Keyword Arguments:
            params {list} -- The parameters to use when executing the SQL statement. (default: {None})
        """

        if params == None: self.conn.execute(statement)

        else: self.conn.execute(statement,params)

    def close(self,do_commit=False):
        """Closes the database connection, commiting the changes if necessary.
        
        Keyword Arguments:
            do_commit {boolean} -- True if the database changes should be committed. (default: {False})
        """

        if do_commit: self.conn.commit()

        self.conn.close()