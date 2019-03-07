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

from .input_util import InputUtil
from models import database
from models import DatabaseInfo
from models import Job
from models import Prop
from models import Recipient


class DbUtil(object):

    @staticmethod
    def check_db():

        '''
        Db Ok if:

            No tables are missing
            One of the records in the Props table is selected
            No errors occur when making the checks.
        '''

        error = None

        db_ok = False

        try:

            # Collect any missing tables
            missing_tables = [
                table
                for table
                in [DatabaseInfo, Prop, Job, Recipient]
                if not table.table_exists()
            ]

            db_ok = not missing_tables

            if db_ok:

                # Determine if there are any Prop records
                all_props = Prop.select()

                if all_props:

                    # Determine if there are any selected Prop records
                    selected_props = [
                        prop
                        for prop
                        in all_props
                        if prop.is_selected
                    ]

                    if not selected_props:

                        error = Exception(
                            f'''
                            No selected records in the Prop table,
                            which are required for sending emails to recipients.
                            Please run job_finder with the --setup flag.
                            '''
                        )

                        db_ok = False

                else:

                    error = Exception(
                        f'''
                        No records in the Prop table,
                        which are required for sending emails to recipients.
                        Please run job_finder with the --setup flag.
                        '''
                    )

        except Exception as e:

            error = e

        if error:

            raise Exception(
                f'''
                The following error was thrown when trying to connect to the database:

                    {str(error)}
                '''
            )

        return db_ok

    @staticmethod
    def create_tables():
        """Check Database Connection"""

        tables_created = True

        try:

            missing_tables = [
                table
                for table
                in [DatabaseInfo, Prop, Job, Recipient]
                if not table.table_exists()
            ]

            existing_tables = [
                table
                for table
                in [DatabaseInfo, Prop, Job, Recipient]
                if table not in missing_tables
            ]

            if 0 < len(missing_tables) and len(missing_tables) < 5:

                for table in existing_tables:

                    if table.select():

                        # TODO: Improve this message.
                        raise Exception(
                            '''
                            Some, but not all of the required tables exist.
                            Some of the existing tables contain records.
                            The database is only partially formed.
                            Please backup the data you'd like to keep,
                            delete the existing tables then try again.
                            '''
                        )

            database.create_tables(
                [
                    DatabaseInfo,
                    Job,
                    Recipient,
                    Prop
                ]
            )

        except Exception as e:

            logging.getLogger().error(f'Error while creating tables: {str(e)}')

            tables_created = False

        return tables_created

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

            logging.getLogger().error('No email properties selected in the database Prop table!')

            raise Exception('No email properties selected in the database Prop table!')

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