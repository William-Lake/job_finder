from job_emailer import job_emailer
from recipient import recipient
from job import job

print('Creating job & recipient objects')
rcp = recipient([0,'william.lake@mail.helenacollege.edu',0.0])

jb = job([0,0,0,'Test Job Title','Test Job Dept','Test Job URL'])

print('Creating job emailer.')
mailer = job_emailer()

print('Notifying recipients of job.')
mailer.notify_recipients_of_job([rcp,],jb)