# Job Finder

A set of python scripts built to gather State of Montana IT jobs in Helena, MT on behalf of students in the UM Helena IT department, notifying them of a new job if one appears.

Job data gathered from the State of Montana's [central job site](https://mtstatejobs.taleo.net/careersection/200/jobsearch.ftl?lang=en).

## Requirements

This project was built using Python 2.7, on Ubuntu 16.04. 

If you're on a Windows system, I recommend [this guide](https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation) to get your Python environment variables set up.

### Modules used

- [sqlite3](https://docs.python.org/2/library/sqlite3.html)
- [requests](http://docs.python-requests.org/en/master/)
- [lxml](http://lxml.de/), specifically [html](http://lxml.de/lxmlhtml.html)
- [time](https://docs.python.org/2/library/time.html)
- [urllib](https://docs.python.org/2/library/urllib.html)

## Getting started

1. Open a Command Line/Terminal Session
2. Ensure you have python 2.7 installed before continuing. If not get it installed.

```bash
python --version
```

2. Clone this repository

```bash
git clone https://www.github.com/William-Lake/job_finder.git
```

3. Enter the repo's directory

```bash
cd job_finder
```

3. Create a local copy of the database

```bash
sqlite3 Helena_Jobs.db < Create_DB.sql
```

4. Create a python script that imports job_finder

```python
from job_finder import job_finder
```

5. Create a job_finder object

```python
jf = job_finder()
```

6. Add/Remove recipient emails from the database

```python
jf.add_recipient('Test.Person@email.net')

jf.remove_recipient('Sad.Sack@email.net')
```

7. Gather/Review current jobs and notify recipients

```python
jf.gather_and_review_jobs()
```

## Database

The database used for this project is sqlite. The included Create_DB.sql script shows the current database structure.

## TODO

- ~~Review current job id hashcode method, consider changing it.~~
    - This works fine.
- ~~At the moment there isn't any process for notifying recipients. A method exists in recipient.py, but it doesn't do anything. The original idea was to send an email. I currently have a [gist saved](https://gist.github.com/William-Lake/6eb8d8f5b08e0251b5df3589ead788a4) re: how to complete this but I'm uncertain if it's the best way. *This needs to be resolved.*~~
    - See job_emailer.py
    - ~~**Currently undergoing testing, not working at the moment.**~~
    - **UPDATE: 03/02/2018** Resolved
- Once the email notification issue has been resolved, the idea is to drop everything onto a web server and set up a cronjob to execute the job_finder script nightly.
    - [Potentially useful gist](https://gist.github.com/William-Lake/f50758f07a28f097fda78172379ecb63)
- When this all gets set up on a web server, will need a web service/input page to handle gathering the user's email and adding it to the database- *after verifying they are allowed to do so.*
    - Best way to verify?
- Instead of deleting jobs from the database, they should be saved in a 'job_history' table with a 'date_opened' and 'date_closed' field.
- ~~Add a method to notify users when a job *closes*.~~

## Moving Forward

This repo currently only gathers State of Montana IT Jobs. It would be useful to combine this functionality with jobs gathered from the private and/or non-profit sector.

Additionally, it will likely be useful at some point to provide a web interface to display the currently gathered jobs.

[This list](https://github.com/toddmotto/public-apis#jobs) has some potentially useful apis that could help with this.
