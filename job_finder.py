"""
Job Finder

Gathers IT Jobs from the State of Montana,
which are located in Helena, MT, 
and notifies a group of users about it.

Built for the IT students of UM Helena.
"""

import requests
from lxml import html
import time
import urllib
import sqlite3
from db_connection import db_connection
from job import job
from recipient import recipient

class job_finder(object):

	def __init__(self):
		"""Constructor"""

		self.db_conn = db_connection()

		self.load_recipients()

		self.gather_current_jobs()

		self.review_jobs()

		self.db_conn.close(True)

	def add_recipient(self,email):
		"""Adds the given recipient's email to the database of recipients.
		
		Arguments:
			email {str} -- The recipients email to add to the database.
		"""
		
		recipient_data = [email,time.time()]

		new_recipient = recipient(recipient_data)

		new_recipient.insert(self.db_conn)

		self.recipients.append(new_recipient)

	def remove_recipient(self,email):
		"""Removes the given recipient's email from the database of recipients.
		
		Arguments:
			email {str} -- The recipients email to remove from the database.
		"""

		recipient_data = [email,time.time()]

		recipient_to_delete = recipient(recipient_data)

		recipient_to_delete.delete(self.db_conn)

		recipients_to_save = []

		for current_recipient in self.recipients:

			if current_recipient.email != email: recipients_to_save.append(current_recipient)

		self.recipients = recipients_to_save

	def load_recipients(self):
		"""Loads all the recipients in the database."""

		self.recipients = []

		recipients_data = self.db_conn.execute_select('SELECT * FROM recipient')

		for recipient_data in recipients_data:

			self.recipients.append(recipient(recipient_data))

	def gather_current_jobs(self):
		"""Gathers all the currently saved jobs in the database."""

		self.current_jobs = []

		statement = 'SELECT * FROM job'

		jobs_data = self.db_conn.execute_select(statement)

		for job_data in jobs_data:

			self.current_jobs.append(job(job_data))

	def review_jobs(self):
		"""Gathers all the jobs from the State of MT jobs site,
		saving those that are new,
		and deleting those that have expired.
		"""

		jobs_to_delete = self.check_for_new_jobs()

		self.delete_old_jobs(jobs_to_delete)

	def check_for_new_jobs(self):
		"""Checks the State of MT Jobs site for new jobs,
		saving the new ones, and gathering those that should
		be deleted from the database.
		
		Returns:
			list -- The of jobs to delete.
		"""

		jobs_on_site = []

		url = 'https://mtstatejobs.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=101430233'

		headers = {'Content-Type':'application/json','Accept':'application/json'}

		payload = {"multilineEnabled":'false',"sortingSelection":{"sortBySelectionParam":"5","ascendingSortingOrder":"true"},"fieldData":{"fields":{"KEYWORD":"","LOCATION":"","ORGANIZATION":""},"valid":'true'},"filterSelectionParam":{"searchFilterSelections":[{"id":"POSTING_DATE","selectedValues":[]},{"id":"LOCATION","selectedValues":["20300100198"]},{"id":"JOB_FIELD","selectedValues":["7000100198"]}]},"advancedSearchFiltersSelectionParam":{"searchFilterSelections":[{"id":"ORGANIZATION","selectedValues":[]},{"id":"LOCATION","selectedValues":[]},{"id":"JOB_FIELD","selectedValues":[]},{"id":"STUDY_LEVEL","selectedValues":[]},{"id":"WILL_TRAVEL","selectedValues":[]},{"id":"JOB_SHIFT","selectedValues":[]}]},"pageNo":1}

		response = requests.post(url, json=payload)

		json_data = response.json()

		jobs_data = json_data['requisitionList']

		for job_data in jobs_data:

			site_id = job_data['jobId']

			contest_num = job_data['contestNo']

			site_url = 'https://mtstatejobs.taleo.net/careersection/200/jobdetail.ftl?job={}'.format(contest_num)

			target_data = job_data['column']

			title = target_data[0]

			dept = target_data[2]

			job_id = hash(site_id + contest_num + site_url + title + dept)

			new_job = job([job_id,site_id,contest_num,title,dept,site_url])

			jobs_on_site.append(new_job)

			if new_job.job_in_db(self.db_conn): 
				
				new_job.insert(self.db_conn)

				self.current_jobs.append(new_job)

				self.notify_recipients(new_job)

		return list(set(self.current_jobs).difference(jobs_on_site))

	def delete_old_jobs(self,old_jobs):
		"""Deletes the given set of jobs from the database.
		
		Arguments:
			old_jobs {list} -- The old jobs to delete.
		"""

		for old_job in old_jobs: 
			
			old_job.delete(self.db_conn)

			self.current_jobs.remove(old_job)

	def notify_recipients(self,new_job):
		"""Notifies all recipients in the database about a new job.
		
		Arguments:
			new_job {job} -- The job to notify recipeints of.
		"""

		if len(self.recipients) == 0: self.load_recipients()

		for current_recipient in self.recipients: current_recipient.notify(new_job)

def main():
	"""Main method"""

	jf = job_finder()

if __name__ == '__main__': main()