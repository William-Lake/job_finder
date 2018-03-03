"""Emails recipients about new jobs."""

import smtplib
from email.mime.text import MIMEText
import sys
from recipient import recipient
from job import job

class job_emailer(object):

    def __init__(self):
        """Constructor"""

        self.load_access_data()

    def load_access_data(self):
        """Loads the data necessary to login to an email account so emails can be sent from it."""

        try: 
            # Read in the Access_Data.txt file to a list.
            # One line in Access_Data.txt = One item in the list.
            access_data = open('Access_Data.txt').readlines()

        except:

            print("This module requires a file called 'Access_Data.txt' in its directory which contains the username and password to a gmail account.")

        # Iterate through the lines of data read in from Access_Data.txt, saving what's appropriate.
        for line in access_data:

            # Want to skip lines that are comments, blank, or don't contain the equals sign.
            if line.startswith('#') or len(line.strip()) == 0 or '=' not in line: continue

            # The format of each line with useful data is Key=Value
            access_items = line.split('=')

            data_type = access_items[0].strip().upper()

            data = access_items[1].strip()

            if data_type == 'EMAIL': self.email = data

            elif data_type == 'PASSWORD': self.password = data

            elif data_type == 'SMTP': self.smtp = data

            elif data_type == 'PORT': self.port = data

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

        self.craft_message()

        self.send_email()

    def create_email_body(self):
        """Creates the email body using the data from the job object."""

        if self.is_new: self.msg_data = 'NEW JOB\n'

        else: self.msg_data = 'JOB CLOSED\n'

        self.msg_data += 'Title: {}\n'.format(self.job.title)

        self.msg_data += 'Dept.: {}\n'.format(self.job.dept)

        self.msg_data += 'Full Posting: {}\n'.format(self.job.site_url)

    def gather_recipient_emails(self):
        """Gathers the recipients' emails into a comma delimited string."""
        '''
        self.recipient_emails = []

        for recipient in self.recipients: 
            
            self.recipient_emails.append(recipient.email)
        '''
        self.recipient_emails = ''

        for recipient in self.recipients: 
            
            self.recipient_emails += recipient.email + ','

        self.recipient_emails = self.recipient_emails[:-1]

    def craft_message(self):
        """Crafts a locally-sourced, artisinal email message."""

        self.msg = MIMEText(self.msg_data,self.text_subtype)

        if self.is_new: self.msg['Subject'] = 'New Job Posted: {}'.format(self.job.title)

        else: self.msg['Subject'] = 'Job Closed: {}'.format(self.job.title)

        self.msg['From'] = self.email

        self.msg['To'] = self.recipient_emails

    def send_email(self):
        """Sends the created email."""

        try:

            smtpObj = smtplib.SMTP_SSL(self.smtp, self.port)

            smtpObj.login(user=self.email,password=self.password)

            smtpObj.sendmail(self.email,self.recipient_emails, self.msg.as_string())

            smtpObj.quit()

        except smtplib.SMTPException as error:

            print('ERROR Unable to send email : {err}'.format(err=error))