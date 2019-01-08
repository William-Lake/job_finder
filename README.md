# Job Finder

>Original Author | Credit : [William Lake](https://github.com/William-Lake/job_finder)

A set of python scripts built to gather State of Montana IT jobs in Helena, MT on behalf of students in the UM Helena IT department, notifying them of a new job if one appears.

Job data gathered from the State of Montana's [central job site](https://mtstatejobs.taleo.net/careersection/200/jobsearch.ftl?lang=en).

## Requirements

This project was built using Python 3.6, on Ubuntu 18.04, and tested
on Win-10 via [conda](https://conda.io/docs/) virtual environments.

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
1. Ensure you have python 3 installed before continuing. If not [get it installed](https://wiki.python.org/moin/BeginnersGuide/Download).

    ```shell
    python --version
    ```

1. Clone this repository

    ```shell
    git clone https://www.github.com/William-Lake/job_finder.git
    ```

1. Enter the repository and install with `pip`.

    ```shell
    # Dont forget the "." after -e

    cd job_finder
    pip install -e .
    ```

1. Add recipient and generate database.

    ```shell
    # Note: change email address to the desired recipient.

    jobfinder ADD email@nowhere.com
    ```

## Usage

The entry point for the application is aptly called, `jobfinder`. The purpose of this script is to manage interaction with the parser, recipient, and smtp email-sender.

### Using the Driver script

The `jobfinder` script provides three main functions:

- Add a recipient
- Remove a recipient
- Gather jobs/Review jobs/Notify recipients

#### Add a recipient

To add a new recipient you would execute the `jobfinder` script, passing in the `ADD` keyword followed by the recipient's email address, like so:

```shell
jobfinder ADD test@email.com
```

You can also add a list of recipients, however **they need to be in a .txt file with one recipient per line.**

```shell
jobfinder ADD recipients_to_add.txt
```

#### Remove a recipient

To remove a recipient you would execute the `jobfinder` script, passing in the `REMOVE` keyword followed by the recipient's email address, like so:

```shell
jobfinder REMOVE test@email.com
```

You can also remove a list of recipients, however **they need to be in a .txt file with one recipient per line.**

```shell
jobfinder ADD recipients_to_remove.txt
```

#### Gather jobs/Review jobs/Notify recipients

To perform the default `Job_Finder` functions, you would execute the `jobfinder` script with no arguments:

```shell
jobfinder
```

## Notifying recipients

`Job_Finder` uses `Job_Emailer` to notify recipients of jobs that have either closed or opened recently.

In order to do so, `Job_Emailer` needs a useable email address and password, as well as smtp and port info. This information is stored ina  database tabled named `jobfinder.db` for SQLite3, and in a Schema named `jobs` in
the default `PostgreSQL` installation.

Access to the SQLite3 Database can be found at the following locations:

```shell
For Windows

C:\Users\%username%\AppData\Local\jobfinder\jobfinder.db

For Linux | MacOSX
$HOME/.local/share/jobfinder/jobfinder.db
```

The data required for the `props` table (SQLite | PostgreSQL) is as follows:

```shell
SMTP=test.server.net
PORT=1234
EMAIL=email@test.net
PASSWORD=password
```

**NOTE** that your password will be in plain text. **This is not secure and will be addressed in future iterations.** Additionally, `Job_Emailer` has only been tested with one email and may not work with others.

## Database

The database used for this project (currently) is sqlite. The included `sqlite.sql` script shows the current database structure.

## Moving Forward

This repository currently only gathers State of Montana IT Jobs. It would be useful to combine this functionality with jobs gathered from the private and/or non-profit sector.

Additionally, it will likely be useful at some point to provide a web interface to display the currently gathered jobs.

[This list](https://github.com/toddmotto/public-apis#jobs) has some potentially useful apis that could help with this.
