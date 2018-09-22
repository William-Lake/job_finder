# Job Finder

A set of python scripts built to gather State of Montana IT jobs in Helena, MT on behalf of students in the UM Helena IT department, notifying them of a new job if one appears.

Job data gathered from the State of Montana's [central job site](https://mtstatejobs.taleo.net/careersection/200/jobsearch.ftl?lang=en).

## Requirements

This project was built using Python 3.6, on Ubuntu 18.04. 

If you're on a Windows system, I recommend [this guide](https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation) to get your Python environment variables set up.

### Modules used

- [os](https://docs.python.org/3.6/library/os.html)
- [sys](https://docs.python.org/3.6/library/sys.html)
- [time](https://docs.python.org/3.6/library/time.html)
- [logging](https://docs.python.org/3.6/howto/logging.html)
- [requests](http://docs.python-requests.org/en/master/)
- [urllib](https://docs.python.org/3.6/library/urllib.html)
- [smtplib](https://docs.python.org/3.6/library/smtplib.html)
- [lxml](http://lxml.de/), specifically [html](http://lxml.de/lxmlhtml.html)
- [sqlite3](https://docs.python.org/3.6/library/sqlite3.html)

## Getting started

1. Open a Command Line/Terminal Session
2. Ensure you have python 3 installed before continuing. If not [get it installed](https://wiki.python.org/moin/BeginnersGuide/Download).

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

Job Finder has an included `Driver` script whose intent is to manage interaction with the `job_finder` module.

### Using the Driver script

The `Driver` script provies three main functions:

- Add a recipient
- Remove a recipient
- Gather jobs/Review jobs/Notify recipients

#### Add a recipient

To add a new recipient you would execute the `Driver` script, passing in the `ADD` keyword followed by the recipient's email address, like so:

```bash
python Driver.py ADD test@email.com
```

You can also add a list of recipients, however **they need to be in a .txt file with one recipient per line.**

```bash
python Driver.py ADD recipients_to_add.txt
```

#### Remove a recipient

To remove a recipient you would execute the `Driver` script, passing in the `REMOVE` keyword followed by the recipient's email address, like so:

```bash
python Driver.py REMOVE test@email.com
```

You can also remove a list of recipients, however **they need to be in a .txt file with one recipient per line.**

```bash
python Driver.py ADD recipients_to_remove.txt
```

#### Gather jobs/Review jobs/Notify recipients

To perform the default `Job_Finder` fuctions, you would execute the `Driver` script with no arguments:

```bash
python Driver.py
```

## Notifying recipients

`Job_Finder` uses `Job_Emailer` to notify recipients of jobs that have either closed or opened recently.

In order to do so, `Job_Emailer` needs a useable email address and password, as well as smtp and port info. All of this info needs to be stored in [job_finder_props.py](job_finder_props.py) setting the appropriate values for each variable, like so:

```
SMTP=test.server.net
PORT=1234
EMAIL=email@test.net
PASSWORD=password
```

**NOTE** that your password will be in plain text. **This is not secure and will be addressed in future iterations.** Additionally, `Job_Emailer` has only been tested with one email and may not work with others.

## Database

The database used for this project is sqlite. The included Create_DB.sql script shows the current database structure.

## Moving Forward

This repo currently only gathers State of Montana IT Jobs. It would be useful to combine this functionality with jobs gathered from the private and/or non-profit sector.

Additionally, it will likely be useful at some point to provide a web interface to display the currently gathered jobs.

[This list](https://github.com/toddmotto/public-apis#jobs) has some potentially useful apis that could help with this.
