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

    DEFAULT_CONFIG_FILE = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)), 'logging.conf')

    def __init__(self, args):

        # TODO: Figure out how to address the user wanting to use a different password.

        self.__args = args

        self.__load_configuration()

        self.__logger = logging.getLogger()

        self.__logger.info('JobFinder Initialized')

    def __load_configuration(self, config_file=DEFAULT_CONFIG_FILE):
        """
        Loads logging configuration from the given configuration file.

        Code from: https://github.com/storj/storj-python-sdk/blob/master/tests/log_config.py

        Code found via: https://www.programcreek.com/python/example/105587/logging.config.fileConfig

        :param config_file:
            the configuration file (default=/etc/package/logging.conf)
        :type config_file: str
        """

        # TODO: Figure out why the logging file wasn't loading

        logging.basicConfig(level=logging.DEBUG)

        # if (
        #     not os.path.exists(config_file) or
        #         not os.path.isfile(config_file)):

        #     msg = '%s configuration file does not exist!', config_file

        #     logging.getLogger().error(msg)

        #     raise ValueError(msg)

        # try:
        #     fileConfig(config_file, disable_existing_loggers=False)

        #     logging.getLogger().info('%s configuration file was loaded.',
        #                              config_file)

        # except Exception as e:

        #     logging.getLogger().error('Failed to load configuration from %s!',
        #                               config_file)

        #     logging.getLogger().debug(str(e), exc_info=True)

        #     raise e

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

        # TESTING ===================================
        # saved_jobs, closed_jobs = JobUtil().gather_and_review_jobs()

        # if saved_jobs or closed_jobs:

        #     self.__logger.info('Notifying Recipients')

        #     email_util = EmailUtil()

        #     for job in saved_jobs:

        #         email_util.notify_recipients_of_job(job, EmailUtil.OPENED)

        #     for job in closed_jobs:

        #         email_util.notify_recipients_of_job(job, EmailUtil.CLOSED)

        # exit()
        # TESTING ===================================

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

                    email_util.notify_recipients_of_job(job, EmailUtil.OPENED)

                for job in closed_jobs:

                    email_util.notify_recipients_of_job(job, EmailUtil.CLOSED)

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

                if self.__args.use_recip_file:

                    recipient_util.add_from_file(self.__args.recipients[0])

                else:

                    recipient_util.add(self.__args.recipients)

            elif self.__args.remove_recip:

                if self.__args.use_recip_file:

                    recipient_util.remove_from_file(self.__args.recipients[0])

                else:

                    recipient_util.remove(self.__args.recipients)

# ========================================================================================


def main(args):

    # TESTING =================================================

    # Always check the DB first before any actions to help prevent errors
    # DbUtil.check_db()

    # job_finder = JobFinder(args)

    # try:

    #     job_finder.start()

    # except Exception as e:

    #     logging.getLogger().error(
    #         f'''
    #         There was an error during JobFinder execution:

    #             {str(e)}
    #         '''
    #     )

    # TESTING =================================================

    # Always check the DB first before any actions to help prevent errors
    DbUtil.check_db()

    if args.setup:

        DbUtil.create_tables()

        DbUtil.determine_user_props()

    else:

        job_finder = JobFinder(args)

        try:

            job_finder.start()

        except Exception as e:

            logging.getLogger().error(
                f'''
                There was an error during JobFinder execution:

                    {str(e)}
                '''
            )
