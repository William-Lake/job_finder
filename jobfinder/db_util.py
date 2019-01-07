# -*- coding: utf-8 -*-
# Copyright (C) 2018 William Lake
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


import time
import logging

# update for packaging, use . relative path identifiers
from .db_connection import Db_Connection
from .job import Job
from .recipient import Recipient

class Db_Util(object):

    def __init__(self):
        """Constructor"""

        self.logger = logging.getLogger()

        self.db_connection = Db_Connection()

    def gather_current_recipients(self):
        """Gathers all the currently saved recipients in the database."""
        
        self.logger.debug('Gathering Recipients')

        recipients = []

        recipients_data = self.db_connection.execute_select('SELECT * FROM recipient')

        for recipient_data in recipients_data:

            recipient_id = recipient_data[0]

            email = recipient_data[1]

            date_added = recipient_data[2]

            recipients.append(Recipient(recipient_id,email,date_added))

        self.logger.debug('{} Recipients Gathered'.format(len(recipients)))

        return recipients

    def gather_current_jobs(self):
        """Gathers all the currently saved jobs in the database."""

        self.logger.debug('Gathering Current Jobs')

        current_jobs = []

        statement = 'SELECT * FROM job WHERE date_closed IS NULL'

        jobs_data = self.db_connection.execute_select(statement)

        if jobs_data is not None:

            for job_data in jobs_data:

                job_id = job_data[0]

                site_id = job_data[1]

                contest_num = job_data[2]

                title = job_data[3]

                dept = job_data[4]

                site_url = job_data[5]

                current_jobs.append(Job(job_id,site_id,contest_num,title,dept,site_url))

        self.logger.debug('{} Jobs Gathered'.format(len(current_jobs)))

        return current_jobs

    def save_jobs(self,jobs_to_save):
        """Saves the given jobs to the database.
        
        Arguments:
            jobs_to_save {list} -- The jobs to save in the database.
        """

        self.logger.debug('Saving {} Jobs'.format(len(jobs_to_save)))

        self.saved_jobs = jobs_to_save

        for job in jobs_to_save:

            statement = 'INSERT INTO job (id,site_id,contest_num,title,dept,site_url,date_opened) VALUES (?,?,?,?,?,?,?)'

            params = (job.job_id, job.site_id, job.contest_num, job.title, job.dept, job.site_url,time.time())

            self.db_connection.execute_insert(statement,params)            

    def delete_jobs(self,jobs_to_delete):
        """'Deletes' the given jobs from the database.

        Instead of deleting jobs, the jobs are marked as 'closed'.
        
        Arguments:
            jobs_to_delete {list} -- The jobs to 'Delete' from the database.
        """

        self.logger.debug('Deleting {} Jobs'.format(len(jobs_to_delete)))

        self.deleted_jobs = jobs_to_delete

        for job in jobs_to_delete:

            statement = 'UPDATE job SET date_closed = ? WHERE id = ?'

            params = (time.time(),job.job_id)

            self.db_connection.execute_update(statement,params)

    def add_recipient(self,email):
        """Adds the given recipient to the database.
        
        Arguments:
            email {str} -- The email to add to the database.
        """
        self.logger.debug('Adding Recipient: ' + email)

        statement = 'INSERT INTO recipient (email,date_added) VALUES (?,?)'

        params = (email, time.time())

        self.db_connection.execute_insert(statement,params)

    def remove_recipient(self,email):
        """Removes the given recipient from the database.
        
        Arguments:
            email {str} -- The email to remove from the database.
        """
        self.logger.debug('Removing Recipient: ' + email)

        statement = 'DELETE FROM recipient WHERE email = ?'

        params = (email,)

        self.db_connection.execute_delete(statement, params)

    def close_connection(self):
        """Closes the connection to the database."""

        self.db_connection.close()
