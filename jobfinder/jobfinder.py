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

import sys
import os
import logging
from argparse import ArgumentParser

from logging.config import fileConfig
from job_util import JobUtil
from db_util import Dbutil
from recipient_util import RecipientUtil
from email_util import EmailUtil

class JobFinder(object):
    '''Manages the process of gathering jobs from the state of montana job site.'''

    DEFAULT_CONFIG_FILE = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)), 'logging.conf')

    def __init__(self, args):

        self.__args = args

        # Always check the DB first before any actions to help prevent errors
        Dbutil.check_db()

        self.__load_configuration()

        self.__logger = logging.getLogger()

        try:

            self.__start()

        except Exception as err:

            self.__logger.exception(
                'There was an error during finder execution: %r' % err)

    def __load_configuration(self, config_file=DEFAULT_CONFIG_FILE):
        """
        Loads logging configuration from the given configuration file.

        Code from: https://github.com/storj/storj-python-sdk/blob/master/tests/log_config.py

        Code found via: https://www.programcreek.com/python/example/105587/logging.config.fileConfig

        :param config_file:
            the configuration file (default=/etc/package/logging.conf)
        :type config_file: str
        """
        if (
            not os.path.exists(config_file) or 
            not os.path.isfile(config_file)):

            msg = '%s configuration file does not exist!', config_file

            logging.getLogger().error(msg)

            raise ValueError(msg)

        try:
            fileConfig(config_file, disable_existing_loggers=False)

            logging.getLogger().info('%s configuration file was loaded.',
                                     config_file)

        except Exception as e:

            logging.getLogger().error('Failed to load configuration from %s!',
                                      config_file)

            logging.getLogger().debug(str(e), exc_info=True)

            raise e

    def __start(self):

        '''
        If the user passed in a file or some recipients,
        but add and remove are both false,
        throw an error.
        '''

        if (
            not self.__args.add_recip and
            not self.__args.remove_recip and
            self.__args.recipients
        ):

            self.__logger.warning('Recipients provided but no instruction about what to do with them!')

            raise Exception('Recipients provided but no instruction about what to do with them! Please use the -h flag to determine what arguments to pass to job_finder.')

        elif (
            not self.__args.add_recip and
            not self.__args.remove_recip and
            not self.__args.recipients
        )

            self.__logger.debug('No args passed.')

            saved_jobs, closed_jobs = JobUtil().gather_and_review_jobs()

            if saved_jobs or closed_jobs:

                self.__logger.info='Notifying Recipients'

                email_util = EmailUtil()

                for job in saved_jobs: 
                    
                    email_util.notify_recipients_of_job(job, EmailUtil.OPENED)

                for job in closed_jobs: 
                    
                    email_util.notify_recipients_of_job(job, EmailUtil.CLOSED)

        else:

            recipient_util = RecipientUtil()

            if self.__args.add_recip:

                if self.__args.use_recip_file: 
                    
                    recipient_util.add_recipients_from_file(self.__args.recipients[0])

                else:

                    recipient_util.add_recipients(self.__args.recipients)

            elif self.__args.remove_recip:

                if self.__args.use_recip_file: 
                    
                    recipient_util.remove_recipients_from_file(self.__args.recipients[0])

                else:

                    recipient_util.remove_recipients(self.__args.recipients)

# ========================================================================================

def gather_args():

    arg_parser = ArgumentParser(description='Gathers and notifies recipients about IT jobs at the State of Montana.')

    arg_parser.add_argument(
        '--add_recip',
        action='store_true',
        help='Whether the following recipients or recipient file should be added to the database.'
    )

    arg_parser.add_argument(
        '--remove_recip',
        action='store_true',
        help='Whether the following recipients or recipient file should be removed from the database.'
    )

    arg_parser(
        '--use_recip_file',
        action='store_true',
        help='Whether a file of emails is being provided to the job_finder. NOTE: .txt files only, one email per line.'
    )

    arg_parser(
        'recipients',
        nargs='*',
        help='One or more recipient emails, or file(s) containing the emails that should be (added to/removed from) the database.'
    )

    return arg_parser.parse_args()

def main():

    args = gather_args()

    job_finder = JobFinder(args)
