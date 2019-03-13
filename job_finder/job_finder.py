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

    def __init__(self, args):
        '''Constructor
        
        Arguments:
            args {list} -- The command line arguments passed in during execution.
        '''

        # TODO: Figure out how to address the user wanting to use a different password.

        self.__args = args

        self.__logger = logging.getLogger()

        # Checking the Database
        # We want to let outside executors to know if it's ok to continue program execution after these checks.
        self.do_execute = True

        # Always check the DB first before any actions to help prevent errors
        db_ok = DbUtil.check_db()

        if not db_ok:

            self.__logger.info('Creating JobFinder Tables.')

            tables_created = DbUtil.create_tables()

            if not tables_created:

                self.do_execute = False

                self.__logger.info('Error during JobFinder Table Creation.')

            else:

                self.__logger.info('JobFinder Initialized')

    def start(self):

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
            not self.__args.add_recip and
            not self.__args.remove_recip and
            not self.__args.recipients
        ):

            # NORMAL JOB_FINDER EXECUTION

            self.__logger.debug('No args passed.')

            saved_jobs, closed_jobs = JobUtil().gather_and_review_jobs()

            if saved_jobs or closed_jobs:

                self.__logger.info('Notifying Recipients')

                email_util = EmailUtil()

                for job in saved_jobs:

                    # TODO Remove pass, uncomment email line.

                    pass

                    # email_util.notify_recipients_of_job(job, EmailUtil.OPENED)

                for job in closed_jobs:

                    # TODO Remove pass, uncomment email line.

                    pass

                    # email_util.notify_recipients_of_job(job, EmailUtil.CLOSED)

        elif (
            not self.__args.add_recip and
            not self.__args.remove_recip and
            self.__args.recipients
        ):

            # ERROR - RECIPIENTS W/O DIRECTION

            self.__logger.warning('Recipients provided but no instruction about what to do with them!')

            raise Exception('Recipients provided but no instruction about what to do with them! Please use the -h flag to determine what arguments to pass to job_finder.')

        elif (
            (self.__args.add_recip or
            self.__args.remove_recip) and
            not self.__args.recipients
        ):

            # ERROR - RECIPIENTS W/O DIRECTION

            self.__logger.warning('Recipient instructions provided without recipients to work with!')

            raise Exception('Recipient instructions provided without recipients to work with! Please use the -h flag to determine what arguments to pass to job_finder.')

        else:

            # ALTERING USERS

            self.__logger.info('Altering Recipients')

            recipient_util = RecipientUtil()

            recipient_emails, recipient_files = self.__gather_recip_emails_and_files(self.__args.recipients)

            if self.__args.add_recip:

                recipient_util.add(recipient_emails)

                recipient_util.add_from_files(recipient_files)

            elif self.__args.remove_recip:

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

    if args.setup:

        tables_created = DbUtil.create_tables()

        if tables_created:

            DbUtil.determine_user_props()

        else:

            # Can't use the logger b/c it hasn't been set up at this stage.
            print('Error during JobFinder Table Creation.')

    else:

        job_finder = JobFinder(args)

        # We need to know if it's safe to execute before trying to do so.
        if job_finder.do_execute:

            try:

                job_finder.start()

            except Exception as e:

                logging.getLogger().error(
                    f'''
                    There was an error during JobFinder execution:

                        {str(e)}
                    '''
                )
