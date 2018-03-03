"""Database Util

Manages database interactions.
"""


import time
from db_connection import db_connection
from job import job
from recipient import recipient

class db_util(object):

    def __init__(self):
        """Constructor"""

        self.db_conn = db_connection()

    def gather_current_recipients(self):
        """Gathers all the currently saved recipients in the database."""
        
        recipients = []

        recipients_data = self.db_conn.execute_select('SELECT * FROM recipient')

        for recipient_data in recipients_data:

            recipients.append(recipient(recipient_data))

        return recipients

    def gather_current_jobs(self):
        """Gathers all the currently saved jobs in the database."""

        current_jobs = []

        statement = 'SELECT * FROM job WHERE date_closed IS NULL'

        jobs_data = self.db_conn.execute_select(statement)

        for job_data in jobs_data:

            current_jobs.append(job(job_data))

        return current_jobs

    def save_jobs(self,jobs_to_save):
        """Saves the given jobs to the database.
        
        Arguments:
            jobs_to_save {list} -- The jobs to save in the database.
        """

        self.saved_jobs = jobs_to_save

        for job in jobs_to_save:

            statement = 'INSERT INTO job (id,site_id,contest_num,title,dept,site_url,date_opened) VALUES (?,?,?,?,?,?)'

            params = (job.job_id, job.site_id, job.contest_num, job.title, job.dept, job.site_url,time.time())

            self.db_conn.execute_insert(statement,params)            

    def delete_jobs(self,jobs_to_delete):
        """'Deletes' the given jobs from the database.

        Instead of deleting jobs, the jobs are marked as 'closed'.
        
        Arguments:
            jobs_to_delete {list} -- The jobs to 'Delete' from the database.
        """

        self.deleted_jobs = jobs_to_delete

        for job in jobs_to_delete:

            statement = 'UPDATE job SET date_closed = ? WHERE id = ?'

            params = (job.job_id,time.time())

            self.db_conn.execute_update(statement,params)

    def add_recipient(self,email):
        """Adds the given recipient to the database.
        
        Arguments:
            email {str} -- The email to add to the database.
        """

        statement = 'INSERT INTO recipient (email,date_added) VALUES (?,?)'

        params = (email, time.time())

        self.db_conn.execute_insert(statement,params)

    def remove_recipient(self,email):
        """Removes the given recipient from the database.
        
        Arguments:
            email {str} -- The email to remove from the database.
        """

        statement = 'DELETE FROM recipient WHERE email = ?'

        params = (email,)

        self.db_conn.execute_delete(statement, params)

    def close_connection(self):
        """Closes the connection to the database."""

        self.db_conn.close()