"""
Job

Represents an IT Job found in Helena, MT.

"""

class Job(object):

    def __init__(self,job_id,site_id,contest_num,title,dept,site_url):
        """Constructor
        
        Arguments:
            job_data {list} -- The list of job data to use when building this job object.
        """

        self.job_id = job_id

        self.site_id = site_id

        self.contest_num = contest_num

        self.title = title

        self.dept = dept

        self.site_url = site_url