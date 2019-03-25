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

from datetime import datetime
import logging
import requests

from models import Job


class JobUtil(object):
    '''Performs the common Job related functions.'''

    def __init__(self):
        """Constructor"""

        self.__logger = logging.getLogger()

        self.__logger.info('JobUtil Initialized')

    def gather_and_review_jobs(self):
        """Gathers the jobs from the web,
        compares them to the ones in the database,
        and saves/returns the changes found.
        """
        self.__logger.info('Gathering and Reviewing Jobs')

        self.__gather_jobs_on_site()

        self.__close_jobs()

        self.__save_jobs()

        return self.__saved_jobs, self.__closed_jobs

    def __gather_jobs_on_site(self):
        """Grabs the jobs from the State of MT website."""

        self.__logger.info('Gathering Jobs From Site')

        self.__jobs_on_site = []

        # Prepare everything necessary to gather the webpage data.
        url = 'https://mtstatejobs.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=101430233'

        headers = {
            'Host': 'mtstatejobs.taleo.net',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://mtstatejobs.taleo.net/careersection/200/jobsearch.ftl',
            'Content-Type': 'application/json', 'tz': 'GMT-06:00',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': '702'
        }

        payload = {
            "multilineEnabled": 'false',
            "sortingSelection": {
                "sortBySelectionParam": "5",
                "ascendingSortingOrder": "true"
            },
            "fieldData": {
                "fields": {
                    "KEYWORD": "",
                    "LOCATION": "",
                    "ORGANIZATION": ""
                },
                "valid": 'true'
            },
            "filterSelectionParam": {
                "searchFilterSelections": [
                    {
                        "id": "POSTING_DATE",
                        "selectedValues": []
                    },
                    {
                        "id": "LOCATION",
                        "selectedValues": ["20300100198"]
                    },
                    {
                        "id": "JOB_FIELD",
                        "selectedValues": ["7000100198"]
                    }
                ]
            },
            "advancedSearchFiltersSelectionParam": {
                "searchFilterSelections": [
                    {
                        "id": "ORGANIZATION",
                        "selectedValues": []
                    },
                    {
                        "id": "LOCATION",
                        "selectedValues": []
                    },
                    {
                        "id": "JOB_FIELD",
                        "selectedValues": []
                    },
                    {
                        "id": "STUDY_LEVEL",
                        "selectedValues": []
                    },
                    {
                        "id": "WILL_TRAVEL",
                        "selectedValues": []
                    },
                    {
                        "id": "JOB_SHIFT",
                        "selectedValues": []
                    }
                ]
            },
            "pageNo": 1
        }

        session = requests.Session()

        # Set up session/cookies
        session.get(
            'https://mtstatejobs.taleo.net/careersection/200/jobsearch.ftl?lang=en')

        cookie_dict = session.cookies.get_dict()

        headers['Cookie'] = f'locale={cookie_dict["locale"]}; JSESSIONID={cookie_dict["JSESSIONID"]}'

        response = session.post(
            url,
            headers=headers,
            json=payload
        )

        if response.status_code == 200:

            json_data = response.json()

            # Pull out just the jobs data from the webpage data.
            jobs_data = json_data['requisitionList']

            # Iterate through the jobs data.
            for job_data in jobs_data:
                # Generated by the state, used to identify the job.
                site_id = int(job_data['jobId'])

                # Generated by the state, used to identify the job's webpage.
                contest_num = int(job_data['contestNo'])

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

                # Create a job object with the collected data.
                new_job = Job(
                    site_id=site_id,
                    contest_num=contest_num,
                    title=title,
                    dept=dept,
                    site_url=site_url,
                    date_opened=datetime.today()
                )

                self.__jobs_on_site.append(new_job)

        else:

            self.__logger.error(
                'Taleo response code != 200: ' + str(response.status_code))

    def __save_jobs(self):
        """From the list of jobs that have been pulled from the web, finds those
        that need to be saved.
        """
        self.__logger.info('Finding Jobs to Save')

        # Create a list of the job ids for open jobs in the database.
        db_open_job_nums = [
            job.contest_num
            for
            job in Job.select().where(Job.date_closed == None)
        ]

        # We need only the jobs that aren't in the database already,
        self.__saved_jobs = [
            job
            for
            job in self.__jobs_on_site
            if job.contest_num not in db_open_job_nums
        ]

        # And we need to save them.
        for job in self.__saved_jobs:
            
            job.save()

        self.__logger.info(f'Saved {len(self.__saved_jobs)} jobs.')

    def __close_jobs(self):
        """From the list of jobs that have been pulled from the web,
        finds those that need to be closed.
        """
        self.__logger.info('Finding Jobs to close')

        # Create a list of the job ids for open jobs in the database.
        site_job_nums = [
            job.contest_num
            for
            job in self.__jobs_on_site
        ]

        # We need to compare what's current in the db vs what's current on the site.
        db_open_jobs = Job.select().where(Job.date_closed == None)

        self.__closed_jobs = [
            job
            for
            job in db_open_jobs
            if job.contest_num not in site_job_nums
        ]

        # We need to update the jobs in the database.
        for job in self.__closed_jobs:

            job.date_closed = datetime.today().strftime('%Y-%m-%d')

            job.save()

            self.__closed_jobs.append(job)

        self.__logger.info(f'Closed {len(self.__closed_jobs)} jobs.')
