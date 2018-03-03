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
2. Ensure you have python 2.7 installed before continuing. If not [get it installed](https://wiki.python.org/moin/BeginnersGuide/Download).

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

3. Create a local copy of the database, if necessary.

```bash
sqlite3 Helena_Jobs.db < Create_DB.sql
```

## Usage

Job Finder has an included `Driver` script whose intent is to manage interaction with the `job_finder` module. You can either make use of the Driver script, or you can use `job_finder` directly.

### Using the Driver script

Just like `job_finder`, the `Driver` script provies three main functions:

- Add a recipient
- Remove a recipient
- Gather jobs/Review jobs/Notify recipients

#### Add a recipient

To add a new recipient you would execute the `Driver` script, passing in the `ADD` keyword followed by the recipient's email address, like so:

```bash
python Driver.py ADD test@email.com
```

#### Remove a recipient

To remove a recipient you would execute the `Driver` script, passing in the `REMOVE` keyword followed by the recipient's email address, like so:

```bash
python Driver.py REMOVE test@email.com
```

#### Gather jobs/Review jobs/Notify recipients

To perform the default `job_finder` fuctions, you would execute the `Driver` script with no arguments:

```bash
python Driver.py
```

### Using job_finder directly

`job_finder` can be used directly as a class object. To do so:

1. Create a python script that imports `job_finder`

```python
from job_finder import job_finder
```

2. Create a `job_finder` object

```python
jf = job_finder()
```

3. Add/Remove recipient emails from the database as desired

```python
jf.add_recipient('Test.Person@email.net')

jf.remove_recipient('Sad.Sack@email.net')
```

4. Gather/Review current jobs and notify recipients

```python
jf.gather_and_review_jobs()
```

## Notifying recipients

`job_finder` uses `job_emailer` to notify recipients of jobs that have either closed or opened recently.

In order to do so, `job_emailer` needs a useable email address and password, as well as smtp and port info. All of this info needs to be stored in [Access_Data.txt](Access_Data.txt) in a key=value format, like so:

```
SMTP=test.server.net
PORT=1234
EMAIL=email@test.net
PASSWORD=password
```

**NOTE:** `job_emailer` has only been tested with one email and may not work.

## Database

The database used for this project is sqlite. The included Create_DB.sql script shows the current database structure.

## TODO

- Test `job_emailer` with other email accounts.
- Once the email notification issue has been resolved, the idea is to drop everything onto a web server and set up a cronjob to execute the `job_finder` script nightly.
    - [Potentially useful gist](https://gist.github.com/William-Lake/f50758f07a28f097fda78172379ecb63)
- When this all gets set up on a web server, will need a web service/input page to handle gathering the user's email and adding it to the database- *after verifying they are allowed to do so.*
    - Best way to verify incoming emails?

## Moving Forward

This repo currently only gathers State of Montana IT Jobs. It would be useful to combine this functionality with jobs gathered from the private and/or non-profit sector.

Additionally, it will likely be useful at some point to provide a web interface to display the currently gathered jobs.

[This list](https://github.com/toddmotto/public-apis#jobs) has some potentially useful apis that could help with this.
