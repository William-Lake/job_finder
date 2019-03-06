from datetime import datetime
import logging
import os

from models import Recipient


class RecipientUtil(object):

    def __init__(self):

        self.__logger = logging.getLogger()

        self.__logger.info('RecipientUtil Initialized')

    def add_from_files(self, file_names):

        for file_name in file_names:

            if self.__file_ok(file_name):

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

    def remove_from_files(self, file_names):

        for file_name in file_names:

            if self.__file_ok(file_name):

                self.__logger.info(f'Removing Recipients in {file_name}.')

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

    def __file_ok(self, file_name):

        file_name = file_name.strip()

        file_ok = True

        if not os.path.exists(file_name):

            self.__logger.error(f"{file_name} doesn't exist!")

            file_ok = False

        if not file_name.endswith('.txt'):

            self.__logger.error(f"{file_name} isn't a .txt file!")

            file_ok = False

        return file_ok
