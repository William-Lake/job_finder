import time
from db_connection import db_connection
from job import job
from recipient import recipient

class db_util(object):

    def __init__(self):

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

		statement = 'SELECT * FROM job'

		jobs_data = self.db_conn.execute_select(statement)

		for job_data in jobs_data:

			current_jobs.append(job(job_data))

        return current_jobs

    def save_jobs(self,jobs_to_save):

        self.saved_jobs = jobs_to_save

        for job in jobs_to_save:

            statement = 'INSERT INTO job (id,site_id,contest_num,title,dept,site_url) VALUES (?,?,?,?,?,?)'

            params = (job.job_id, job.site_id, job.contest_num, job.title, job.dept, job.site_url)

            db_conn.execute_insert(statement,params)            

    def delete_jobs(self,jobs_to_delete):

        self.deleted_jobs = jobs_to_delete

        for job in jobs_to_delete:

            statement = 'DELETE FROM job WHERE id = ?'

            params = (job.job_id,)

            db_conn.execute_delete(statement,params)

    def add_recipient(self,email):

        statement = 'INSERT INTO recipient (email,date_added) VALUES (?,?)'

        params = (email, time.time())

        db_conn.execute_insert(statement,params)

    def remove_recipient(self,email):
        
        statement = 'DELETE FROM recipient WHERE email = ?'

        params = (self.email,)

        db_conn.execute_delete(statement, params)

    def close_connection(self):

        self.db_conn.close()