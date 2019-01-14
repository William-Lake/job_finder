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
import os
import shutil
import sqlite3
import sys
import time

from os.path import expanduser
from models import *

# This variable should comde from __init__.py but it's not working yet.
DATABASE = 'jobfinder.db'


class Dbutil(object):

    def __init__(self):
        """Constructor"""

        self.logger = logging.getLogger()

    @staticmethod
    def make_dirs():
        """Make directory for the Database"""
        if sys.platform == 'win32':
            location = os.path.abspath(os.path.join(
                expanduser("~"), 'AppData', 'Local', 'jobfinder'))
        else:
            location = os.path.abspath(os.path.join(
                expanduser("~"), '.local', 'share', 'jobfinder'))

        if os.path.exists(location):
            shutil.rmtree(location)
        os.makedirs(location)

    @staticmethod
    def check_db():
        """Check Database Connection

        Actions Performed:
            1. Connect to database
            2. If the database does not exist, create it with init_db()

        Returns
            Tuple from the first row in DB

        """
        if os.path.isfile(Dbutil.get_db_path()):
            try:
                Dbutil.get_db_version()
                return "Database Status = OK"
            except NameError as err:
                raise err
        else:
            Dbutil.init_db()

    @staticmethod
    def init_db():
        """Create Job Finder Database

        Actions Performed:
            1. Open SQLit3 Database connection
            2. Execute SQL query to create tables
            3. Add script information to appdata table
        """
        # get location of the sqlite init script
        sql_file = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)), 'resources/sqlite.sql')

        # make the directories first
        Dbutil.make_dirs()

        # Connect to SQLite3 database
        with sqlite3.connect(Dbutil.get_db_path()) as conn:
            cur = conn.cursor()
            fd = open(sql_file, 'r')
            script = fd.read()
            cur.executescript(script)
            fd.close()

            # get SQLite Version
            cur.execute('SELECT SQLITE_VERSION()')
            sv = cur.fetchone()
            print(f"SQLite Version => {sv}")
        # close connection
        conn.close()

    @staticmethod
    def get_props():
        """Returns Array[1:4] Props for Emailer

        Returns
            smtp[1], port[2], email[3] and pword[4]
        """
        try:
            conn = sqlite3.connect(Dbutil.get_db_path())
            cur = conn.cursor()
            cur.execute('SELECT * FROM props WHERE ROWID = 1')
            data = cur.fetchone()
            conn.close()
            return data
        except sqlite3.OperationalError as sql3_error:
            print(f"Failed fetchall on props => {sql3_error}")
            sys.exit(2)

    @staticmethod
    def get_db_version():
        """Get Job FinderDatabase Version

        Retruns
            Tuple row from appdata

        """
        dbv = ""
        try:
            with sqlite3.connect(Dbutil.get_db_path()) as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM appdata '
                            'ORDER BY ROWID ASC LIMIT 1')
                for row in cur.fetchall():
                    dbv = row[3]
            conn.close()
            return dbv
        except sqlite3.OperationalError as sql3_error:
            print(f"Fetchrow failed=> {sql3_error}")
            Dbutil.init_db()

    @staticmethod
    def get_db_path():
        """Get AppData Directory based on Platform"""
        if sys.platform == 'win32':
            db_name = os.path.abspath(os.path.join(
                expanduser("~"), 'AppData', 'Local',
                'jobfinder', DATABASE))
        else:
            db_name = os.path.abspath(os.path.join(
                expanduser("~"), '.local', 'share',
                'jobfinder', DATABASE))

        return db_name
