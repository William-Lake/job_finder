from datetime import datetime
import logging
import os

from models import Recipient


class RecipientUtil(object):
    '''Performs common Recipient related actions.'''
    
    def __init__(self):
        '''Constructor'''

        self.__logger = logging.getLogger()

        self.__logger.info('RecipientUtil Initialized')

    def add_from_files(self, file_names):
        '''Adds all the recipients in the files contained in the given list.
        
        Arguments:
            file_names {list} -- A list of filenames, each containing recipient emails to save.
        '''

        recipient_emails = self.__gather_emails_from_files(file_names)

        self.add(recipient_emails)

    def add(self, recipient_emails):
        '''Adds all the recipient in the given list to the database.
        
        Arguments:
            recipient_emails {list} -- The list of recipient emails.
        '''

        self.__logger.info(f'Adding {len(recipient_emails)} recipients.')

        for email in recipient_emails:

            Recipient.create(
                email=email.strip(),
                date_added=datetime.today().strftime('%Y-%m-%d')
            )

    def remove_from_files(self, file_names):
        '''Removes all the recipients in the files contained in the given list.
        
        Arguments:
            file_names {list} -- A list of filenames, each containing recipient emails to remove.
        '''
        recipient_emails = self.__gather_emails_from_files(file_names)

        self.remove(recipient_emails)

    def remove(self, recipient_emails):
        '''Removes all the recipient in the given list from the database.
        
        Arguments:
            recipient_emails {list} -- The list of recipient emails.
        '''
        self.__logger.info(f'Removing {len(recipient_emails)} recipients.')

        for email in recipient_emails:

            recipient = Recipient.get_or_none(Recipient.email == email.strip())

            if recipient:

                recipient.delete_instance()

            else:

                self.__logger.warning(
                    f'Recipient {email} was not in the database.'
                )

    def __gather_emails_from_files(self,file_names):
        '''Gathers all the emails from all the given list of files.
        
        Arguments:
            file_names {list} -- The list of file_names to gather emails from.
        
        Returns:
            list -- The list of recipient emails gathered from the listed files.
        '''

        recipient_emails = []

        for file_name in file_names:

            file_name = file_name.strip()

            # We want to make sure the file exists and is a .txt file.
            if (
                os.path.exists(file_name) and
                file_name.endswith('.txt')
            ):

                for email in open(file_name).readlines():

                    email = email.strip()

                    recipient_emails.append(email)

            else:

                self.__logger.error(f"{file_name} either doesn't exist or isn't a .txt file!")

        return recipient_emails