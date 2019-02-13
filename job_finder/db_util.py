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
"""Database Util

Manages database interactions.
"""
import logging

from input_util import InputUtil
from models import database
from models import DatabaseInfo
from models import Job
from models import Prop
from models import Recipient

# This variable should comde from __init__.py but it's not working yet.
DATABASE = 'jobfinder.db'


class DbUtil(object):

    @staticmethod
    def check_db():

        logger = logging.getLogger()

        db_ok = False

        try:

            logger.debug('Checking if database & tables exist.')

            if database.get_tables():

                db_ok = True
                
        except Exception as e:

            logger.error("Database doesn't exist!")

            raise Exception(
                f'''
                The following error was thrown when trying to connect to the database:

                    {str(e)}

                If you haven't already, please create a PostGreSQL database and provide the connection information in the job_finder_props.py file.
                '''
            )

        return db_ok

    @staticmethod
    def create_tables():
        """Check Database Connection"""

        logger = logging.getLogger()

        try:

            logger.debug('Checking if database & tables exist.')

            if not database.get_tables():

                logger.debug('Creating database tables.')

                try:

                    database.create_tables(
                        [
                            DatabaseInfo,
                            Job,
                            Recipient,
                            Prop
                        ]
                    )

                except Exception as e:

                    logger.error(f'Error while trying to create tables: {str(e)}')

                    print(
                        f'''
                        There was an error while trying to create the database:

                            {str(e)}
                        '''
                    )
                
        except Exception as e:

            logger.error("Database doesn't exist!")

            raise Exception(
                f'''
                The following error was thrown when trying to connect to the database:

                    {str(e)}

                If you haven't already, please create a PostGreSQL database and provide the connection information in the job_finder_props.py file.
                '''
            )

    @staticmethod
    def get_props():
        """Returns Array[1:4] Props for Emailer

        Returns
            smtp[1], port[2], email[3] and pword[4]
        """

        prop = Prop.get_or_none(Prop.is_selected == True)

        if prop:

            return prop.smtp, prop.port, prop.email, prop.pword

        else:

            logging.getLogger().error('No email properties in the database Prop table!')

            raise Exception('No email properties in the database Prop table!')

    @staticmethod
    def determine_user_props():

        existing_props = Prop.select()

        '''
        If there's already properties
            Ask the user if they want to use an existing one
                If so, let them choose
                if not, give them the option to create a new one
            Otherwise give them the option to createa  new one
        '''
        if existing_props:

            use_existing = InputUtil.gather_boolean_input(
                f'There are {len(existing_props)} properties in the database already. Would you like to use one of them?',
                true_option='Y',
                false_option='N'
            )

            if use_existing:

                prop_options = {}

                for prop in existing_props:

                    prop.is_selected = False

                    prop.save()

                    prop_options[prop.email] = prop

                prop_selection = InputUtil.gather_selection_input(prop_options)

                prop_selection.is_selected = True

                prop_selection.save()

            else:

                DbUtil.gather_user_props()

        else:

            DbUtil.gather_user_props()

    @staticmethod
    def gather_user_props():

        prop = Prop()

        for item in ['SMTP', 'PORT', 'EMAIL', 'PASS']:

            prompt = f'{item}?'

            user_input = (
                InputUtil.gather_input(prompt)
                if item != 'PASS'
                else InputUtil.gather_input(prompt, is_password=True)
            )

            if item == 'SMTP':

                prop.smtp = user_input

            elif item == 'PORT':

                prop.port = user_input

            elif item == 'EMAIL':

                prop.email = user_input

            else:

                prop.pword = user_input

        prop.is_selected = True

        prop.save()
