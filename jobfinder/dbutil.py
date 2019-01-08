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
from jobfinder import dbconnect, job, recipient
from .job import Job
from .recipient import Recipient

# This variable should comde from __init__.py but it's not working yet.
DATABASE = 'jobfinder.db'


class Dbutil(object):

    def __init__(self):
        """Constructor"""

        self.logger = logging.getLogger()

        self.conn = dbconnect.Dbconnection()

    def gather_current_recipients(self):
        """Gathers all the currently saved recipients in the database."""

        self.logger.debug('Gathering Recipients')

        recipients = []

        recipients_data = self.conn.execute_select('SELECT * FROM recipient')

        for recipient_data in recipients_data:
            recipient_id = recipient_data[0]

            email = recipient_data[1]

            date_added = recipient_data[2]

            recipients.append(Recipient(recipient_id, email, date_added))

        self.logger.debug('{} Recipients Gathered'.format(len(recipients)))

        return recipients

    def gather_current_jobs(self):
        """Gathers all the currently saved jobs in the database."""

        self.logger.debug('Gathering Current Jobs')

        current_jobs = []

        statement = 'SELECT * FROM job WHERE date_closed IS NULL'

        jobs_data = self.conn.execute_select(statement)

        if jobs_data is not None:

            for job_data in jobs_data:
                job_id = job_data[0]

                site_id = job_data[1]

                contest_num = job_data[2]

                title = job_data[3]

                dept = job_data[4]

                site_url = job_data[5]

                current_jobs.append(
                    Job(job_id, site_id, contest_num, title, dept, site_url))

        self.logger.debug('{} Jobs Gathered'.format(len(current_jobs)))

        return current_jobs

    def save_jobs(self, jobs_to_save):
        """Saves the given jobs to the database.
        
        Arguments:
            jobs_to_save {list} -- The jobs to save in the database.
        """

        self.logger.debug('Saving {} Jobs'.format(len(jobs_to_save)))

        self.saved_jobs = jobs_to_save

        for job in jobs_to_save:
            statement = 'INSERT INTO job (id, site_id, contest_num, title, ' \
                        'dept, site_url, date_opened) VALUES (?,?,?,?,?,?,?)'

            params = (job.job_id, job.site_id, job.contest_num, job.title,
                      job.dept, job.site_url, time.time())

            self.conn.execute_insert(statement, params)

    def delete_jobs(self, jobs_to_delete):
        """'Deletes' the given jobs from the database.

        Instead of deleting jobs, the jobs are marked as 'closed'.
        
        Arguments:
            jobs_to_delete {list} -- The jobs to 'Delete' from the database.
        """

        self.logger.debug('Deleting {} Jobs'.format(len(jobs_to_delete)))

        self.deleted_jobs = jobs_to_delete

        for job in jobs_to_delete:
            statement = 'UPDATE job SET date_closed = ? WHERE id = ?'

            params = (time.time(), job.job_id)

            self.conn.execute_update(statement, params)

    def add_recipient(self, email):
        """Adds the given recipient to the database.
        
        Arguments:
            email {str} -- The email to add to the database.
        """
        self.logger.debug('Adding Recipient: ' + email)

        statement = 'INSERT INTO recipient (email,date_added) VALUES (?,?)'

        params = (email, time.time())

        self.conn.execute_insert(statement, params)

    def remove_recipient(self, email):
        """Removes the given recipient from the database.
        
        Arguments:
            email {str} -- The email to remove from the database.
        """
        self.logger.debug('Removing Recipient: ' + email)

        statement = 'DELETE FROM recipient WHERE email = ?'

        params = (email,)

        self.conn.execute_delete(statement, params)

    def close_connection(self):
        """Closes the connection to the database."""

        self.conn.close()

    @staticmethod
    def get_user_home():
        """Return User Home Directory"""

        return expanduser("~")

    @staticmethod
    def make_dirs():
        """Make directory for the Database"""
        if sys.platform == 'win32':
            location = os.path.abspath(os.path.join(
                Dbutil.get_user_home(), 'AppData', 'Local', 'jobfinder'))
        else:
            location = os.path.abspath(os.path.join(
                Dbutil.get_user_home(), '.local', 'share', 'jobfinder'))

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
            print("SQLite Version => {sv}".format(sv=sv))
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
            print("Failed fetchall on props => {sql3_error}".format(
                sql3_error=sql3_error))
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
            print("Fetchrow failed=> {sql3_error}".format(
                sql3_error=sql3_error))
            Dbutil.init_db()

    @staticmethod
    def get_db_path():
        """Get AppData Directory based on Platform"""
        if sys.platform == 'win32':
            db_name = os.path.abspath(os.path.join(
                Dbutil.get_user_home(), 'AppData', 'Local',
                'jobfinder', DATABASE))
        else:
            db_name = os.path.abspath(os.path.join(
                Dbutil.get_user_home(), '.local', 'share',
                'jobfinder', DATABASE))

        return db_name
