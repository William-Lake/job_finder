from datetime import datetime
import logging
import os

from models import Recipient


class RecipientUtil(object):

    def __init__(self):

        self.__logger = logging.getLogger()

        self.__logger.info('RecipientUtil Initialized')

    def add_from_file(self, file_name):

        self.__review_file(file_name)

        self.__logger.info(f'Adding Recipients in {file_name}.')

        recipient_emails = open(file_name).readlines()

        self.add_recipients(recipient_emails)

    def add(self, recipient_emails):

        self.__logger.info(f'Adding {len(recipient_emails)} recipients.')

        for email in recipient_emails:

            Recipient.create(
                email=email.strip(),
                date_added=datetime.today().strftime('%Y-%m-%d')
            )

    def remove_from_file(self, file_name):

        self.__review_file(file_name)

        self.__logger.info('Removing Recipients in ' + file_name)

        recipient_emails = open(file_name).readlines()

        self.remove_recipients(recipient_emails)

    def remove(self, recipient_emails):

        self.__logger.info(f'Removing {len(recipient_emails)} recipients.')

        for email in recipient_emails:

            recipient = Recipient.get_or_none(Recipient.email == email.strip())

            if recipient:

                Recipient.delete_instance()

            else:

                self.__logger.warning(
                    f'Recipient {email} was not in the database.'
                )

    def __review_file(self, file_name):

        file_name = file_name.strip()

        if not os.path.exists(file_name):

            self.__raise_file_exception("Provided file doesn't exist!")

        if not file_name.endswith('.txt'):

            self.__raise_file_exception("Provided file isn't a .txt file!")

    def __raise_file_exception(self, message):

        self.__logger.warning(message)

        raise Exception(message)
