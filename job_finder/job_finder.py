# -*- coding: utf-8 -*-
# Copyright (C) 2018 William Lake, Greg Beam
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""Main Class for finder utility."""

import logging

from util.db_util import DbUtil
from util.email_util import EmailUtil
from util.job_util import JobUtil
from util.recipient_util import RecipientUtil


class JobFinder(object):
    '''Manages the process of gathering jobs from
    the state of montana job site.'''

    def __init__(self):
        '''Constructor
        
        Arguments:
            args {list} -- The command line arguments passed in during execution.
        '''

        # TODO: Figure out how to address the user wanting to use a different password.

        self.__logger = logging.getLogger()

        self.__logger.info('JobFinder Initialized')

    def start(self, args):
        '''Starts JobFinder Execution'''

        '''
        We need to determine what to do based on the command line args
        passed in by the user.

        If no arguments were passed, perform the typical job_finder tasks:

            - Review state of montana jobs site for changes,
            - Store the changes
            - Notify recipients of changes

        If recipients were passed in but no direction on whether they should
        be added or removed, raise an error.

        Otherwise, gather the recipients and add them to/remove them from the
        database as indicated by the user.
        '''

        if (
            not args.add_recip and
            not args.remove_recip and
            not args.recipients
        ):

            # NORMAL JOB_FINDER EXECUTION

            self.__logger.debug('No args passed.')

            saved_jobs, closed_jobs = JobUtil().gather_and_review_jobs()

            if saved_jobs or closed_jobs:

                self.__logger.info('Notifying Recipients')

                email_util = EmailUtil()

                for job in saved_jobs:

                    email_util.notify_recipients_of_job(job, EmailUtil.OPENED)

                for job in closed_jobs:

                    email_util.notify_recipients_of_job(job, EmailUtil.CLOSED)

        elif (
            not args.add_recip and
            not args.remove_recip and
            args.recipients
        ):

            # ERROR - RECIPIENTS W/O DIRECTION

            self.__logger.warning('Recipients provided but no instruction about what to do with them!')

            raise Exception('Recipients provided but no instruction about what to do with them! Please use the -h flag to determine what arguments to pass to job_finder.')

        elif (
            (
                args.add_recip or
                args.remove_recip
            ) and
            not args.recipients
        ):

            # ERROR - RECIPIENTS W/O DIRECTION

            self.__logger.warning('Recipient instructions provided without recipients to work with!')

            raise Exception('Recipient instructions provided without recipients to work with! Please use the -h flag to determine what arguments to pass to job_finder.')

        else:

            # ALTERING USERS

            self.__logger.info('Altering Recipients')

            recipient_util = RecipientUtil()

            recipient_emails, recipient_files = self.__gather_recip_emails_and_files(args.recipients)

            if args.add_recip:

                recipient_util.add(recipient_emails)

                recipient_util.add_from_files(recipient_files)

            elif args.remove_recip:

                recipient_util.remove(recipient_emails)

                recipient_util.remove_from_files(recipient_files)

    def __gather_recip_emails_and_files(self,recipients):
        '''Separates the provided recipients into emails and .txt files.

        This is necessary since Job_Finder currently allows users to pass
        in bare emails along with .txt files containing multiple emails in
        any order they'd like.
        
        Arguments:
            recipients {list} -- The list of recipient emails/.txt files to parse.
        
        Returns:
            list -- The list of bare recipient emails.
            list -- The list of recipient email .txt files.
        '''

        recipient_emails = [
            recipient
            for recipient
            in recipients
            if '@' in recipient
        ]

        recipient_files = [
            recipient_file
            for recipient_file
            in recipients
            if '@' not in recipient_file
        ]

        return recipient_emails, recipient_files

# ========================================================================================


def main(args):
    '''Job_Finder Main Method
    
    Arguments:
        args {NameSpace} -- The argparse.ArgumentParser NameSpace containing the Job_Finding command line arguments.
    '''

    try:

        # We need to know if the user is trying to set up JobFinder.
        if args.setup:

            # We want to first create the tables, then determine the email properties.
            tables_created = DbUtil.create_tables()

            # We only want to save email properties if the tables were created,
            if tables_created:

                DbUtil.determine_user_props()

            # Otherwise we need to halt execution.
            else:

                logging.getLogger().error('Error during JobFinder Table Creation.')

        else:

            # We need to see if there's any actions that need to be taken before job_finder can be used.
            db_action = DbUtil.check_db()

            # We need to continue taking action until JobFinder is ready to use.
            while db_action is not None:

                logging.getLogger.info(f'{db_action} must happen before execution can continue.')

                # We need to know if the action was successful so we can decide whether to break out.
                action_successful = db_action()

                if not action_successful:

                    logging.getLogger().error(f'Failure while performing DB Action {db_action}.')

                    # We want to raise an exception to ensure JobFinder isn't started.
                    raise Exception(f'Failure while performing DB Action {db_action}.')

                else:

                    # We need to know if more action is needed. If not, db_action will be None.
                    db_action = DbUtil.check_db()

            # Presuming everything is ready to use, we want to start JobFinder.
            job_finder = JobFinder()

            job_finder.start(args)

    except Exception as e:

        logging.getLogger().error(
            f'''
            There was an error during JobFinder execution:

                {str(e)}
            '''
        )
