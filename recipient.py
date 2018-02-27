"""
Recipient

Represents a recipient of new job notifications.
"""

from db_connection import db_connection

class recipient(object):

    def __init__(self,recipient_data):
        """Constructor
        
        Arguments:
            recipient_data {list} -- The data to use when building this recipient object.
        """

        self.recipient_id = recipient_data[0]

        self.email = recipient_data[1]

        self.date_added = recipient_data[2]

    def insert(self,db_conn):
        """Inserts this recipient into the database.
        
        Arguments:
            db_conn {db_connection} -- The db_connection to use when inserting this recipient into the database.
        """

        statement = 'INSERT INTO recipient (email,date_added) VALUES (?,?)'

        params = (self.email, self.date_added)

        db_conn.execute_insert(statement,params)

    def delete(self,db_conn):
        """Deletes this recipient from the database.
        
        Arguments:
            db_conn {db_connection} -- The db_connection to use when deleting this recipient from the database.
        """

        statement = 'DELETE FROM recipient WHERE email = ?'

        params = (self.email,)

        db_conn.execute_delete(statement, params)

    def notify(self,new_job):
        """Notifies the email associated with this recipient of the given job.
        
        NOTE: This method is not at all complete.

        Arguments:
            new_job {job} -- The job to notify this recipent of.
        """

        # Notify this recipient of the provided job.

        print('Notifying recipient')