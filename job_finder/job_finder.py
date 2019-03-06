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
from logging.config import fileConfig
import os

from db_util import DbUtil
from email_util import EmailUtil
from job_util import JobUtil
from recipient_util import RecipientUtil


class JobFinder(object):
    '''Manages the process of gathering jobs from
    the state of montana job site.'''

    def __init__(self, args):

        # TODO: Figure out how to address the user wanting to use a different password.

        self.__args = args

        self.__logger = logging.getLogger()

        self.__setup()

    def __setup(self):

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

        If recipients were passed in with both the --add and --remove flags,
        raise an error.

        Otherwise, gather the recipients and add them to/remove them from the
        database as indicated by the user.
        '''

        '''
        Regular execution - GOOD
        Regular Execution with no Db - GOOD
        Add one recipient
        Add multiple recipients
        Remove one recipient
        Remove multiple recipients
        Try to both add and remove recipients
        '''

        if (
            not self.__args.add_recip and
            not self.__args.remove_recip and
            not self.__args.recipients
        ):

            self.__logger.debug('No args passed.')

            saved_jobs, closed_jobs = JobUtil().gather_and_review_jobs()

            if saved_jobs or closed_jobs:

                self.__logger.info('Notifying Recipients')

                email_util = EmailUtil()

                for job in saved_jobs:

                    print(job.title)

                    # email_util.notify_recipients_of_job(job, EmailUtil.OPENED)

                for job in closed_jobs:

                    print(job.title)

                    # email_util.notify_recipients_of_job(job, EmailUtil.CLOSED)

        elif (
            not self.__args.add_recip and
            not self.__args.remove_recip and
            self.__args.recipients
        ):

            self.__logger.warning('Recipients provided but no instruction about what to do with them!')

            raise Exception('Recipients provided but no instruction about what to do with them! Please use the -h flag to determine what arguments to pass to job_finder.')

        elif (
            self.__args.add_recip and
            self.__args.remove_recip and
            self.__args.recipients
        ):

            self.__logger.warning('Recipients provided with conflicting instructions!')

            raise Exception('Recipients provided with conflicting instructions! Please use the -h flag to determine what arguments to pass to job_finder.')

        else:

            recipient_util = RecipientUtil()

            if self.__args.add_recip:

                recipients = [
                    recipient
                    for recipient
                    in self.__args.recipients
                    if '@' in recipient
                ]

                recipient_files = [
                    recipient_file
                    for recipient_file
                    in self.__args.recipients
                    if '@' not in recipient_file
                ]

                recipient_util.add(recipients)

                recipient_util.add_from_files(recipient_files)

            elif self.__args.remove_recip:

                recipients = [
                    recipient
                    for recipient
                    in self.__args.recipients
                    if '@' in recipient
                ]

                recipient_files = [
                    recipient_file
                    for recipient_file
                    in self.__args.recipients
                    if '@' not in recipient_file
                ]

                recipient_util.remove(recipients)

                recipient_util.remove_from_files(recipient_files)

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
