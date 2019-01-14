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
"""Emails recipients about new jobs."""

import sys
import logging
import smtplib
from email.mime.text import MIMEText

from jobfinder import dbutil
from .dbutil import Dbutil
from .models import Recipient


class Emailer(object):

    OPENED = 'NEW JOB\n'

    CLOSED = 'JOB CLOSED\n'

    def __init__(self):
        """Constructor"""

        # for debugging props is returning properly
        self.debug = '0'

        self.logger = logging.getLogger()

        self.logger.info('Initializing Job Emailer')

        self.props = dbutil.Dbutil.get_props()

        self.smtp = self.props[1]

        self.port = self.props[2]

        self.email = self.props[3]

        self.password = self.props[4]
        
        # Assumed for now, no current plans to send emails with anything else.
        self.text_subtype = 'plain'
        
        # in debug mode, print props and exit
        if self.debug == '1':

            self.logger.info(self.props)

            print(self.props)

            sys.exit(0)

    def notify_recipients_of_job(self,job,status):
        """Notifies the recipients of a change in job status.
        
        Arguments:
            job {job} -- The job to notify the recipients of.
            status {str} -- The job status to notify the recipients. Only two values acceptable, both as constants: Emailer.OPENED Emailer.CLOSED
        """

        if (
            status != Emailer.OPENED and
            status != Emailer.CLOSED
        ):
            raise Exception('Job status can only be Emailer.OPENED or Emailer.CLOSED.')

        email_body = self.__create_email_body(job,status)

        for recipient in Recipient.select():

            self.__craft_message(job, email_body, recipient.email, status)

            self.__send_email(recipient.email)

    def __create_email_body(self, job, job_status):
        """Creates the email body using the data from the job object."""

        email_body = job_status

        email_body += f'Title: {job.title}\n'

        email_body += f'Dept.: {job.dept}\n'

        email_body += f'Full Posting: {job.site_url}\n'

        return email_body

    def __craft_message(self, job, email_body, recipient_email, status):
        """Creates an email message.
        
        Arguments:
            email_body {str} -- The body of the email.
            recipient_email {str} -- The email of the recipient.
            status {str} -- The status of the job the email is being created for. Either one of two options, Emailer.OPENED or Emailer.CLOSED.
        """

        self.msg = MIMEText(email_body, self.text_subtype)

        self.msg['Subject'] = (
            f'New Job Posted: {job.title}'
            if status == Emailer.OPENED
            else
            f'Job Closed: {job.title}'
        )

        self.msg['From'] = self.email

        self.msg['To'] = recipient_email

    def __send_email(self, email):
        """Sends the created email."""

        try:

            smtpObj = smtplib.SMTP_SSL(self.smtp, self.port)

            smtpObj.login(user=self.email, password=self.password, )

            self.logger.debug(f'Sending to {email}')

            smtpObj.sendmail(self.email, email, self.msg.as_string())

            smtpObj.quit()

        except smtplib.SMTPException as err:

            self.logger.exception('ERROR Unable to send email : %r' % err)
