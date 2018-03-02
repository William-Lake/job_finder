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