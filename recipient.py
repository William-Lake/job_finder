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
