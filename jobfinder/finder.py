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
from datetime import datetime

# update for packaging, use . relative path identifiers
from models import *
from dbutil import Dbutil
from emailer import Emailer


class Finder(object):
    
    def __init__(self, args=None):
        """Constructor"""

        self.__logger = logging.getLogger()

        self.__logger.info('Initializing Job Finder')

        self.__emailer = Emailer()

        self.__args = args

    def start(self):

        # TODO Remove the arg parsing, let JobFinder do it.

        self.__logger.info('Starting Job Finder')

        self.__logger.debug('Parsing args.')

        if self.__args is None:

            self.__logger.debug('No args passed.')

            self.__gather_and_review_jobs()

        else:

            self.__logger.debug('Args passed: ' + ' '.join(self.__args))

            target = self.__args[1].strip()

            if self.__args[0].upper().strip() == 'ADD':

                if target.endswith('.txt'): 
                    
                    self.__add_recipients(target)

                else:

                    Recipient.create(email = target)

            elif self.__args[0].upper().strip() == 'REMOVE':

                if target.endswith('.txt'):

                    self.__remove_recipients(target)

                else:
                    
                    recipient = Recipient.get_or_none(Recipient.email == target)

                    if recipient is not None: Recipient.delete_instance()

                    else: self.__logger.warn(f'User with email ({email}) was not in the database.')

    def __gather_and_review_jobs(self):
        """Gathers the jobs from the web,
        compares them to those in the database,
        and notifies the recipients if necessary.
        """
        self.__logger.info('Gathering and Reviewing Jobs')

        self.__review_jobs()

        self.__notify_recipients()

    def __add_recipients(self, file_name):

        self.__logger.info('Saving Recipients in ' + file_name)

        emails = open(file_name).readlines()

        for email in emails: 

            Recipient.create(
                email = email.strip(), 
                date_added = datetime.today().strftime('%Y-%m-%d'))

    def __remove_recipients(self, file_name):

        self.__logger.debug('Removing Recipients in ' + file_name)

        emails = open(file_name).readlines()

        for email in emails: 

            recipient = Recipient.get_or_none(Recipient.email == email.strip())

            if recipient is not None: Recipient.delete_instance()

            else: self.__logger.warn(f'User with email ({email}) was not in the database.')

    def __review_jobs(self):
        """Gathers all the jobs from the State of MT jobs site,
        saving those that are new,
        and deleting those that have closed.
        """
        self.__logger.info('Reviewing Jobs')

        self.__gather_jobs_on_site()

        self.__save_jobs()

        self.__close_jobs()

    def __gather_jobs_on_site(self):
        """Grabs the jobs from the State of MT website."""

        self.__logger.info('Gathering Jobs From Site')

        self.jobs_on_site = []

        # TODO Consider moving the url, headers, and payload to external files/props

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

        headers['Cookie'] = f'locale={cookie_dict["locale"]}; JSESSIONID={cookie_dict["JSESSIONID"]}'

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
                site_url = f'https://mtstatejobs.taleo.net/careersection/200/jobdetail.ftl?job={contest_num}'

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
                new_job = Job(
                    id = job_id, 
                    site_id = site_id, 
                    contest_num = contest_num, 
                    title = title, 
                    dept = dept,
                    site_url = site_url)

                self.jobs_on_site.append(new_job)

        else:

            self.__logger.error(
                'Taleo response code != 200: ' + str(response.status_code))

    def __save_jobs(self):
        """From the list of jobs that have been pulled from the web, finds those
        that need to be saved.
        """
        self.__logger.info('Finding Jobs to Save')

        # Create a list of the job ids for open jobs in the database.
        current_job_ids = [job.id for job in Job.select().where(Job.date_closed == None)]

        # We need only the jobs that aren't in the database already,
        self.saved_jobs = [job for job in self.jobs_on_site if job.id not in current_job_ids]

        # And we need to save them.
        for job in self.saved_jobs: job.save()

        self.__logger.debug(f'Saved {len(self.saved_jobs)}.')

    def __close_jobs(self):
        """From the list of jobs that have been pulled from the web,
        finds those that need to be closed.
        """
        self.__logger.info('Finding Jobs to close')

        # Create a list of the job ids for open jobs in the database.
        site_job_ids = [job.id for job in self.jobs_on_site]

        # We need to compare what's current in the db vs what's current on the site.
        current_jobs = Job.select().where(Job.date_closed == None)

        self.closed_jobs = [job for job in current_jobs if job.id not in site_job_ids]

        # We need to update the jobs in the database.
        for job in self.closed_jobs

            job.date_closed = datetime.today().strftime('%Y-%m-%d')

            job.save()
            
            self.closed_jobs.append(job)

        self.__logger.debug(f'Closed {len(self.closed_jobs)} jobs.')

    def __notify_recipients(self):
        """Notifies all recipients in the database about a job closing or opening."""

        if len(self.saved_jobs) > 0 or len(self.closed_jobs) > 0:

            self.__logger.info='Notifying Recipients'

            for job in self.saved_jobs: 
                
                self.__emailer.notify_recipients_of_job(job, Emailer.OPENED)

            for job in self.closed_jobs: 
                
                self.__emailer.notify_recipients_of_job(job, Emailer.CLOSED)
