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

import logging
import smtplib
from email.mime.text import MIMEText

import jobfinder.dbutil.Dbutil.get_props as get_props


class Emailer(object):

    def __init__(self):
        """Constructor"""

        props = get_props()

        self.logger = logging.getLogger()
        self.logger.info('Initializing Job Emailer')
        self.smtp = props[1]
        self.port = props[2]
        self.email = props[3]
        self.password = props[4]

        # Assumed for now, no current plans to send emails with anything else.
        self.text_subtype = 'plain'

    def notify_recipients_of_job(self, recipients, job, is_new=True):
        """Notifies the given list of recipients of the given job.
        
        Arguments:
            recipients {list} -- The list of recipients to notify.
            job {job} -- The job to notify the recipients of.
            is_new {boolean} -- True if this is a new job, False if it's a job being closed.
        """

        self.is_new = is_new

        self.job = job

        self.recipients = recipients

        self.create_email_body()

        self.gather_recipient_emails()

        for email in self.recipient_emails:
            self.craft_message(email)

            self.send_email(email)

    def create_email_body(self):
        """Creates the email body using the data from the job object."""

        if self.is_new:
            self.msg_data = 'NEW JOB\n'

        else:
            self.msg_data = 'JOB CLOSED\n'

        self.msg_data += 'Title: {}\n'.format(self.job.title)

        self.msg_data += 'Dept.: {}\n'.format(self.job.dept)

        self.msg_data += 'Full Posting: {}\n'.format(self.job.site_url)

    def gather_recipient_emails(self):
        """Gathers the recipients' emails into a comma delimited string."""

        self.recipient_emails = []

        for recipient in self.recipients:
            self.recipient_emails.append(recipient.email)

    def craft_message(self, email):
        """Crafts a locally-sourced, artisinal email message."""

        self.msg = MIMEText(self.msg_data, self.text_subtype)

        if self.is_new:
            self.msg['Subject'] = 'New Job Posted: {}'.format(self.job.title)

        else:
            self.msg['Subject'] = 'Job Closed: {}'.format(self.job.title)

        self.msg['From'] = self.email

        self.msg['To'] = email

    def send_email(self, email):
        """Sends the created email."""

        try:

            smtpObj = smtplib.SMTP_SSL(self.smtp, self.port)

            smtpObj.login(user=self.email, password=self.password, )

            self.logger.debug('Sending to ' + email)

            smtpObj.sendmail(self.email, email, self.msg.as_string())

            smtpObj.quit()

        except smtplib.SMTPException as err:

            self.logger.exception('ERROR Unable to send email : %r' % err)
