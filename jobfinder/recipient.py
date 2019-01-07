"""
Recipient

Represents a recipient of new job notifications.
"""

class Recipient(object):

    def __init__(self,recipient_id,email,date_added):
        """Constructor
        
        Arguments:
            recipient_data {list} -- The data to use when building this recipient object.
        """

        self.recipient_id = recipient_id

        self.email = email

        self.date_added = date_added
