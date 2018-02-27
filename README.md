# Job Finder

A set of python scripts built to gather State of Montana IT jobs in Helena, MT on behalf of students in the UM Helena IT department, notifying them of a new job if one appears.

Job data gathered from the State of Montana's [central job site](https://mtstatejobs.taleo.net/careersection/200/jobsearch.ftl?lang=en).

## Requirements

This project was built using Python 2.7, on Ubuntu 16.04. 

If you're on a Windows system, I recommend [this guide](https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation) to get your Python environment variables set up.

### Modules used

**All of the following modules are native to Python 2.7+**

- [sqlite3](https://docs.python.org/2/library/sqlite3.html)
- [requests](http://docs.python-requests.org/en/master/)
- [lxml](http://lxml.de/), specifically [html](http://lxml.de/lxmlhtml.html)
- [time](https://docs.python.org/2/library/time.html)
- [urllib](https://docs.python.org/2/library/urllib.html)

## Getting started

1. Clone/Download this repository.
2. Navigate to the downloaded directory for this repo, unzip if necessary, and enter it.
3. If you haven't already, open the directory in a command line/terminal session. 
4. Execute `python job_finder.py`.

## Behind the scenes

When executing `job_finder`:

1. A connection to the sqlite database is created.
2. All recipients are loaded from the database.
3. All currently saved jobs are loaded from the database.
4. All currently posted 'IT' jobs in Helena MT are gathered from the State's job site.
5. Any jobs **found** on the jobs site that **haven't** been saved to the database are saved, and all the current recipients are notified of the new job.
    - **NOTE:***The notification process is not yet complete.*
6. Any jobs **not found** on the jobs site that **have** been saved are deleted from the database.
7. The database connection is closed, committing the changes if directed.

**job_finder also provides the following methods:**

- add_recipient: Adds a given email to the database.
- remove_recipient: Removes a given email from the database.

## Database

The database used for this project is sqlite. The included Create_DB.sql script shows the current database structure.

Instead of an auto-generated id for jobs in the job table, I instead opted to generate a hashcode using all the job data. I'm certain this isnt' the best way, but it's what I went with at the time.

## TODO

- Review current job id hashcode method, consider changing it.
- At the moment there isn't any process for notifying recipients. A method exists in recipient.py, but it doesn't do anything. The original idea was to send an email. I currently have a [gist saved](https://gist.github.com/William-Lake/6eb8d8f5b08e0251b5df3589ead788a4) re: how to complete this but I'm uncertain if it's the best way. *This needs to be resolved.*
- Once the email notification issue has been resolved, the idea is to drop everything onto a web server and set up a cronjob to execute the job_finder script nightly.
    - [Potentially useful gist](https://gist.github.com/William-Lake/f50758f07a28f097fda78172379ecb63)
- When this all gets set up on a web server, will need a web service/input page to handle gathering the user's email and adding it to the database- *after verifying they are allowed to do so.*
    - Best way to verify?
- Instead of deleting jobs from the database, they should be saved in a 'job_history' table with a 'date_opened' and 'date_closed' field.
- Add a method to notify users when a job *closes*.

## Moving Forward

This repo currently only gathers State of Montana IT Jobs. It would be useful to combine this functionality with jobs gathered from the private and/or non-profit sector.

Additionally, it will likely be useful at some point to provide a web interface to display the currently gathered jobs.

[This list](https://github.com/toddmotto/public-apis#jobs) has some potentially useful apis that could help with this.
