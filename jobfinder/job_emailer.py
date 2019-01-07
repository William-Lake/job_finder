"""Emails recipients about new jobs."""

import os
import job_finder_props
import logging
import smtplib
from email.mime.text import MIMEText
import sys
from recipient import Recipient
from job import Job

class Job_Emailer(object):

    def __init__(self):
        """Constructor"""

        self.logger = logging.getLogger()

        self.logger.info('Initializing Job Emailer')

        self.email = job_finder_props.EMAIL

        self.password = job_finder_props.PASSWORD

        self.smtp = job_finder_props.SMTP

        self.port = job_finder_props.PORT

        # Assumed for now, no current plans to send emails with anything else.
        self.text_subtype = 'plain'

    def notify_recipients_of_job(self,recipients,job,is_new=True):
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

        if self.is_new: self.msg_data = 'NEW JOB\n'

        else: self.msg_data = 'JOB CLOSED\n'

        self.msg_data += 'Title: {}\n'.format(self.job.title)

        self.msg_data += 'Dept.: {}\n'.format(self.job.dept)

        self.msg_data += 'Full Posting: {}\n'.format(self.job.site_url)

    def gather_recipient_emails(self):
        """Gathers the recipients' emails into a comma delimited string."""
        
        self.recipient_emails = []

        for recipient in self.recipients: 
            
            self.recipient_emails.append(recipient.email)

    def craft_message(self,email):
        """Crafts a locally-sourced, artisinal email message."""

        self.msg = MIMEText(self.msg_data,self.text_subtype)

        if self.is_new: self.msg['Subject'] = 'New Job Posted: {}'.format(self.job.title)

        else: self.msg['Subject'] = 'Job Closed: {}'.format(self.job.title)

        self.msg['From'] = self.email

        self.msg['To'] = email

    def send_email(self,email):
        """Sends the created email."""

        try:

            smtpObj = smtplib.SMTP_SSL(self.smtp, self.port)

            smtpObj.login(user=self.email,password=self.password)

            self.logger.debug('Sending to ' + email)

            smtpObj.sendmail(self.email,email, self.msg.as_string())

            smtpObj.quit()

        except smtplib.SMTPException as err:

            self.logger.exception('ERROR Unable to send email : %r' % err)