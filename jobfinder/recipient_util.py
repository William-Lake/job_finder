import logging
from datetime import datetime
from models import Recipient

class RecipientUtil(object):

    def __init__(self):

        self.__logger = logging.getLogger()

        self.__logger.info('Initializing RecipientUtil')

    def add_recipients_from_file(self, file_name):

        if not file_name.endswith('.txt'): 

            self.__logger.warning("Provided file isn't a .txt file!")

            raise Exception("Provided file isn't a .txt file!")

        self.__logger.info('Saving Recipients in ' + file_name)

        recipient_emails = open(file_name).readlines()

        self.add_recipients(recipient_emails)

    def add_recipients(self, recipient_emails):

        self.__logger.info(f'Adding {len(recipient_emails)} recipients.')

        for email in recipient_emails:

            Recipient.create(
                email = email.strip(), 
                date_added = datetime.today().strftime('%Y-%m-%d'))

    def remove_recipients_from_file(self, file_name):

        if not file_name.endswith('.txt'): 

            self.__logger.warning("Provided file isn't a .txt file!")

            raise Exception("Provided file isn't a .txt file!")

        self.__logger.info('Removing Recipients in ' + file_name)

        recipient_emails = open(file_name).readlines()

        self.remove_recipients(recipient_emails)

    def remove_recipients(self, recipient_emails):

        self.__logger.info(f'Removing {len(recipient_emails)} recipients.')

        for email in recipient_emails: 

            recipient = Recipient.get_or_none(Recipient.email == email.strip())

            if recipient: Recipient.delete_instance()

            else: self.__logger.warning(f'Recipient {email} was not in the database.')