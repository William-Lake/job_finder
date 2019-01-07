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
"""
Job Finder

Gathers IT Jobs from the State of Montana,
which are located in Helena, MT, 
and notifies a group of users about it.

Built for the IT students of UM Helena.
"""

import sys
import requests
from lxml import html
import time
import urllib
import sqlite3
import logging

# update for packaging, use . relative path identifiers
from .db_util import Db_Util
from .job import Job
from .recipient import Recipient
from .job_emailer import Job_Emailer


class Job_Finder(object):

    def __init__(self, args=None):
        """Constructor"""

        self.logger = logging.getLogger()

        self.logger.info('Initializing Job Finder')

        self.db_util = Db_Util()

        self.conn_closed = False

        self.args = args

    def start(self):

        self.logger.info('Starting Job Finder')

        self.logger.debug('Parsing args.')

        if self.args is None:

            self.logger.debug('No args passed.')

            self.gather_and_review_jobs()

        else:

            self.logger.debug('Args passed: ' + ' '.join(self.args))

            target = self.args[1].strip()

            if self.args[0].upper().strip() == 'ADD':

                if target.endswith('.txt'):
                    self.add_recipients(target)

                else:
                    self.db_util.add_recipient(target)

            elif self.args[0].upper().strip() == 'REMOVE':

                if target.endswith('.txt'):
                    self.remove_recipients(target)

                else:
                    self.db_util.remove_recipient(target)

    def gather_and_review_jobs(self):
        """Gathers the jobs from the web,
        compares them to those in the database,
        and notifies the recipients if necessary.
        """
        self.logger.info('Gathering and Reviewing Jobs')

        self.job_emailer = Job_Emailer()

        self.current_recipients = self.db_util.gather_current_recipients()

        self.current_jobs = self.db_util.gather_current_jobs()

        self.review_jobs()

        self.notify_recipients()

    def add_recipients(self, file_name):

        self.logger.info('Saving Recipients in ' + file_name)

        emails = open(file_name).readlines()

        for email in emails: self.db_util.add_recipient(email.strip())

    def remove_recipients(self, file_name):

        self.logger.debug('Removing Recipients in ' + file_name)

        emails = open(file_name).readlines()

        for email in emails: self.db_util.remove_recipient(email.strip())

    def review_jobs(self):
        """Gathers all the jobs from the State of MT jobs site,
        saving those that are new,
        and deleting those that have closed.
        """
        self.logger.info('Reviewing Jobs')

        self.gather_jobs_on_site()

        self.save_jobs()

        self.delete_jobs()

    def gather_jobs_on_site(self):
        """Grabs the jobs from the State of MT website.
        """

        self.logger.info = 'Gathering Jobs From Site'

        self.jobs_on_site = []

        # Prepare everything necessary to gather the webpage data.
        url = 'https://mtstatejobs.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=101430233'

        headers = {'Host': 'mtstatejobs.taleo.net',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
                   'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Accept-Language': 'en-US,en;q=0.5',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Referer': 'https://mtstatejobs.taleo.net/careersection/200/jobsearch.ftl',
                   'Content-Type': 'application/json', 'tz': 'GMT-06:00',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Content-Length': '702'}

        payload = {"multilineEnabled": 'false',
                   "sortingSelection": {"sortBySelectionParam": "5",
                                        "ascendingSortingOrder": "true"},
                   "fieldData": {"fields": {"KEYWORD": "", "LOCATION": "",
                                            "ORGANIZATION": ""},
                                 "valid": 'true'}, "filterSelectionParam": {
                "searchFilterSelections": [
                    {"id": "POSTING_DATE", "selectedValues": []},
                    {"id": "LOCATION", "selectedValues": ["20300100198"]},
                    {"id": "JOB_FIELD", "selectedValues": ["7000100198"]}]},
                   "advancedSearchFiltersSelectionParam": {
                       "searchFilterSelections": [
                           {"id": "ORGANIZATION", "selectedValues": []},
                           {"id": "LOCATION", "selectedValues": []},
                           {"id": "JOB_FIELD", "selectedValues": []},
                           {"id": "STUDY_LEVEL", "selectedValues": []},
                           {"id": "WILL_TRAVEL", "selectedValues": []},
                           {"id": "JOB_SHIFT", "selectedValues": []}]},
                   "pageNo": 1}

        session = requests.Session()

        # Set up session/cookies
        session.get(
            'https://mtstatejobs.taleo.net/careersection/200/jobsearch.ftl?lang=en')

        cookie_dict = session.cookies.get_dict()

        headers['Cookie'] = 'locale={}; JSESSIONID={}'.format(
            cookie_dict['locale'], cookie_dict['JSESSIONID'])

        response = session.post(url, headers=headers, json=payload)

        if response.status_code == 200:

            json_data = response.json()

            # Pull out just the jobs data from the webpage data.
            jobs_data = json_data['requisitionList']

            # Iterate through the jobs data.
            for job_data in jobs_data:
                # Generated by the state, used to identify the job.
                site_id = job_data['jobId']

                # Generated by the state, used to identify the job's webpage.
                contest_num = job_data['contestNo']

                # The job's full webpage (I.e. contains all the detailed job info.)
                site_url = 'https://mtstatejobs.taleo.net/careersection/200/jobdetail.ftl?job={}'.format(
                    contest_num)

                # Contains the primary job details such as...
                target_data = job_data['column']

                # ...Title...
                title = target_data[0]

                # ... and Department.
                dept = target_data[2]

                # Uncomment this to see what else is included.
                # print(target_data)

                # No way to guarantee that the site_id and contest_num will always be unique, so a hashcode is generated.
                job_id = hash(site_id + contest_num + site_url + title + dept)

                # Create a job object with the collected data.
                new_job = Job(job_id, site_id, contest_num, title, dept,
                              site_url)

                self.jobs_on_site.append(new_job)

        else:

            self.logger.error(
                'Taleo response code != 200: ' + str(response.status_code))

        # TODO: Email yourself/Bryon

    def save_jobs(self):
        """From the list of jobs that have been pulled from the web, finds those
        that need to be saved.
        """
        self.logger.info='Finding Jobs to Save'
        self.jobs_to_save = []
        current_job_ids = self.gather_job_ids(self.current_jobs)

        for job in self.jobs_on_site:
            job_id = job.job_id
            if job_id not in current_job_ids:
                self.jobs_to_save.append(job)

        self.logger.debug(
            'Found {} Jobs To Save'.format(len(self.jobs_to_save)))

        if len(self.jobs_to_save) > 0: self.db_util.save_jobs(self.jobs_to_save)

    def delete_jobs(self):
        """From the list of jobs that have been pulled from the web,
        finds those that need to be deleted.
        """
        self.logger.info = 'Finding Jobs to delete'
        self.jobs_to_delete = []

        site_job_ids = self.gather_job_ids(self.jobs_on_site)

        for job in self.current_jobs:
            if job.job_id not in site_job_ids:
                self.jobs_to_delete.append(job)

        self.logger.debug(
            'Found {} Jobs to Delete'.format(len(self.jobs_to_delete)))

        if len(self.jobs_to_delete) > 0:
            self.db_util.delete_jobs(self.jobs_to_delete)

    def gather_job_ids(self, jobs):
        """Creates a list of job ids from a given list of jobs.

        Arguments:
            jobs {list} -- The jobs to gather the ids from.

        Returns:
            list -- The job ids pulled from the provided jobs.
        """

        job_ids = []

        for job in jobs:
            job_ids.append(job.job_id)

        return job_ids

    def notify_recipients(self):
        """Notifies all recipients in the database about a job closing or opening."""

        if len(self.jobs_to_save) > 0 or len(self.jobs_to_delete) > 0:

            self.logger.info='Notifying Recipients'

            for job in self.db_util.saved_jobs: self.job_emailer.notify_recipients_of_job(
                self.current_recipients, job)

            for job in self.db_util.deleted_jobs: self.job_emailer.notify_recipients_of_job(
                self.current_recipients, job, False)
