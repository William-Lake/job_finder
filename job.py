"""
Job

Represents an IT Job found in Helena, MT.

"""

from db_connection import db_connection

class job(object):

    def __init__(self,job_data):
        """Constructor
        
        Arguments:
            job_data {list} -- The list of job data to use when building this job object.
        """

        self.job_id = job_data[0]

        self.site_id = job_data[1]

        self.contest_num = job_data[2]

        self.title = job_data[3]

        self.dept = job_data[4]

        self.site_url = job_data[5]

    def job_in_db(self,db_conn):
        """Checks if this job is already in the database.
        
        Arguments:
            db_conn {db_connection} -- The db_connection instance to use when checking the database.
        
        Returns:
            boolean -- True if the job is already in the database.
        """

        statement = 'SELECT COUNT(*) FROM job WHERE id = ?'

        params = (self.job_id,)

        result = db_conn.execute_select(statement,params)

        job_count = result.fetchone()

        return job_count > 0

    def insert(self,db_conn):
        """Inserts this job into the database.
        
        Arguments:
            db_conn {db_connection} -- The db_connection instance to use when inserting into the database.
        """

        statement = 'INSERT INTO job (id,site_id,contest_num,title,dept,site_url) VALUES (?,?,?,?,?,?)'

        params = (self.job_id, self.site_id, self.contest_num, self.title, self.dept, self.site_url)

        db_conn.execute_insert(statement,params)

    def delete(self,db_conn):
        """Deletes this job from the database.
        
        Arguments:
            db_conn {db_connection} -- The db_connection instance to use when deleting from the database.
        """

        statement = 'DELETE FROM job WHERE id = ?'

        params = (self.job_id,)

        db_conn.execute_delete(statement,params)