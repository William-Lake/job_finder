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

import logging

from .input_util import InputUtil
from models import database
from models import DatabaseInfo
from models import Job
from models import Prop
from models import Recipient


class DbUtil(object):
    '''DB Utility
    
    Statically manages database interactions.
    '''

    @staticmethod
    def check_db():
        '''Checks if the database is ready for use.
        
        Returns:
            function -- The next DB Action to take, if there is any.
        '''

        db_action = None

        # We first want to know if any tables are missing.
        missing_tables = [
            table
            for table
            in [DatabaseInfo, Prop, Job, Recipient]
            if not table.table_exists()
        ]

        if missing_tables:

            db_action = DbUtil.create_tables

        else:

            # Determine if there are any Prop records
            existing_props = Prop.select()

            if not existing_props:

                db_action = DbUtil.determine_user_props

            else:

                # Determine if there are any selected Prop records
                selected_props = [
                    prop
                    for prop
                    in existing_props
                    if prop.is_selected
                ]

                if (len(selected_props) > 1 or not selected_props):

                    db_action = DbUtil.determine_user_props

        return db_action

    @staticmethod
    def create_tables():
        '''Creates the tables in the database.'''

        tables_created = True

        try:

            # We want to know what tables we need to create.
            missing_tables = [
                table
                for table
                in [DatabaseInfo, Prop, Job, Recipient]
                if not table.table_exists()
            ]

            database.create_tables(missing_tables)

        except Exception as e:

            logging.getLogger().error(f'Error while creating tables: {str(e)}')

            tables_created = False

        return tables_created

    @staticmethod
    def get_props():
        '''Provides the selected Property in the Props table.
        
        Raises:
            Exception -- Raised if there isn't a selected property in the Prop table.
        
        Returns:
            Prop -- The selected property.
        '''

        # We only want the selected Property.
        prop = Prop.get_or_none(Prop.is_selected == True)

        if prop:

            return prop.smtp, prop.port, prop.email, prop.pword

        else:

            logging.getLogger().error('No email properties selected in the database Prop table!')

            raise Exception('No email properties selected in the database Prop table!')

    @staticmethod
    def determine_user_props():
        '''Determines which user property in the database to use.
        
        Returns:
            bool -- True if the process was completed/successful.
        '''

        props_determined = True

        try:

            existing_props = Prop.select()

            '''
            If there's already properties
                Ask the user if they want to use an existing one
                    If so, let them choose
                    if not, give them the option to create a new one
                Otherwise give them the option to create a new one
            '''

            # If there's already properties in the database, we want to let the user know and let them decide which one- if any -to use.
            if existing_props:

                use_existing = InputUtil.gather_boolean_input(f'There are {len(existing_props)} properties in the database already. Would you like to use one of them?')

                if use_existing:

                    prop_options = {}

                    '''
                    We want a dict where the keys are the property's email,
                    and the values are the Property objects,
                    so the InputUtil can use them to determine the user's 
                    Property selection.
                    '''
                    for prop in existing_props:

                        prop.is_selected = False

                        prop.save()

                        prop_options[prop.email] = prop

                    prop_selection = InputUtil.gather_selection_input(prop_options)

                    prop_selection.is_selected = True

                    prop_selection.save()

                else:
                    
                    # We want to get data from the user for a new set of Properties.
                    props_determined = DbUtil.gather_user_props()

            else:

                # We want to get data from the user for a new set of Properties.
                props_determined = DbUtil.gather_user_props()

        except Exception as e:

            logging.getLogger().error(e)

            props_determined = False

        return props_determined

    @staticmethod
    def gather_user_props():
        '''Gathers values from the user and stores them as a Property.

        Returns:
            bool -- True if the process was successful.
        '''

        props_gathered = True

        try:

            prop = Prop()

            # We to collect each item that makes up a Property.
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

        except Exception as e:

            logging.getLogger().error(e)

            props_gathered = False

        return props_gathered
