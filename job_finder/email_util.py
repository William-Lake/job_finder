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

from email.mime.text import MIMEText
import logging
import smtplib

from db_util import DbUtil
from models import Recipient


class EmailUtil(object):

    OPENED = 'NEW JOB\n'

    CLOSED = 'JOB CLOSED\n'

    def __init__(self):
        """Constructor"""

        self.__logger = logging.getLogger()

        self.__logger.info('Initializing Emailer Util')

        self.smtp, self.port, self.email, self.pword = DbUtil.get_props()

        # Assumed for now, no current plans to send emails with anything else.
        self.text_subtype = 'plain'

        self.__logger.info('EmailerUtil Initialized')

    def notify_recipients_of_job(self, job, status):
        """Notifies the recipients of a change in job status.

        Arguments:
            job {job} -- The job to notify the recipients of.
            status {str} -- The job status to notify the recipients.
            Only two values acceptable, both as constants:
                EmailUtil.OPENED
                EmailUtil.CLOSED
        """

        email_body = f'''
        {status}

        Title: {job.title}
        Dept.: {job.dept}
        Full Posting: {job.site_url}
        '''

        # for recipient in Recipient.select():

        #     self.__create_message(job, email_body, recipient.email, status)

        #     self.__send_email(recipient.email)

    def __create_message(self, job, email_body, recipient_email, status):
        """Creates an email message.

        Arguments:
            email_body {str} -- The body of the email.
            recipient_email {str} -- The email of the recipient.
            status {str} -- The status of the job the email is being created
            for. Either one of two options, Emailer.OPENED or Emailer.CLOSED.
        """

        self.msg = MIMEText(email_body, self.text_subtype)

        self.msg['Subject'] = (
            f'New Job Posted: {job.title}'
            if status == EmailUtil.OPENED
            else
            f'Job Closed: {job.title}'
        )

        self.msg['From'] = self.email

        self.msg['To'] = recipient_email

    def __send_email(self, email):
        """Sends the created email."""

        try:

            smtpObj = smtplib.SMTP_SSL(
                self.smtp,
                self.port
            )

            smtpObj.login(
                user=self.email,
                password=self.password,
            )

            self.__logger.debug(f'Sending to {email}')

            smtpObj.sendmail(
                self.email,
                email,
                self.msg.as_string()
            )

            smtpObj.quit()

        except smtplib.SMTPException as e:

            self.__logger.error(f'ERROR Unable to send email : {str(e)}')
