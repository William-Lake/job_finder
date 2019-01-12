# Job Finder

| Application Data ||
| ---| --- |
| Package            | [jobfinder][]
| Version            | 0.1.3
| Topic              | Information Technology, Utilities
| Development Status | 2 - Pre-Alpha
| Compatibility      | Windows, Linux, MacOS
| Arch               | Any
| Python             | Version >= 3.5
| Dependencies       | See [requirements.txt][]

## Page Index

- [Contributors](#contributors)
- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Using the Driver script](#using-the-driver-script)
  - [Add Recipient](#add-recipient)
  - [Remove Recipient](#remove-recipient)
  - [Gather Jobs](#gather-jobs)
  - [Notifying Recipients](#notifying-recipients)
- [Database](#database)
- [Moving Forward](#moving-forward)

## Contributors

- Principal Author : [William Lake][]
- [PyPi][] Packaging : [Greg Beam][]

## Overview

A set of python scripts built to gather State of Montana IT jobs in Helena, MT
on behalf of students in the UM Helena IT department, notifying them of a new
job if one appears. Job data gathered from the State of Montana's
[central job site][].

## Requirements

[Job Finder][] was built using Python >= 3.5, 3.6, 3.7; tested on Ubuntu 18.04
and Windows 10 using [Anaconda Python](https://conda.io/docs/) virtual
environments. For a full list of modules used, see [requirements.txt][]

## Installation

>NOTE: This process is to be used during development. When the package is ready
> for General Availability to the public, a standard `pip install <package-name>`
> will be used rather than the `-e .` convention. Likewise, there will be no
> need to clone the repository beforehand.

A `Makefile` exists for both Windows and Linux | Posix systems. The help message
may look slightly different on each system, however, the commands are identical
for both.

```bash
----------------------------------------
 Job Finder Make Help
----------------------------------------

 The build script takes one option:

   make <option>

   clean      :  clean the build tree
   distclean  :  clean distribution files adn folders
   dist       :  generate distribution wheel
   install    :  install the application locally
   uninstall  :  uninstall the application
   pubtest    :  publish app to test.pypi.org
   publish    :  publish app to pypi.org
   setup      :  pip install requirements.txt
   setupdev   :  pip install requirements-dev.txt

   Example:
     make setup
     make clean
     make install
```

1. Open a Command Line/Terminal Session
1. Change directories to a sutable location and checkout the repository

    ```bash
    git clone https://www.github.com/William-Lake/job_finder.git
    ```

1. Change directories to `job_finder` and install dependencies

    ```bash
    # Install Dependencies in your Virtual Environment

    cd job_finder
    make setup
    ```

1. Add a recipient to initialize the the database.

    ```bash
    # Note: change email address to the desired recipient.

    jobfinder ADD email@nowhere.com
    ```

## Usage

The entry point for the application is aptly called, `jobfinder`. The purpose of
this script is to manage interaction with the parser, recipient, and
smtp-sender.

### Using the Driver script

The `jobfinder` script provides three main functions:

- Add a recipient
- Remove a recipient
- Gather jobs/Review jobs/Notify recipients

### Add Recipient

To add a new recipient you would execute the `jobfinder` script, passing in the
`ADD` keyword followed by the recipient's email address, like so:

```bash
jobfinder ADD test@email.com
```

You can also add a list of recipients, however **they need to be in a .txt file
with one recipient per line.**

```bash
jobfinder ADD recipients_to_add.txt
```

### Remove Recipient

To remove a recipient you would execute the `jobfinder` script, passing in the
`REMOVE` keyword followed by the recipient's email address, like so:

```bash
jobfinder REMOVE test@email.com
```

You can also remove a list of recipients, however, they need to be in a `*.txt`
file with *One Recipient per Line*.

```bash
# Add recipients from file

jobfinder ADD recipients_to_remove.txt
```

### Gather Jobs

To perform the default `Job_Finder` functions, you would execute the `jobfinder`
script with no arguments:

```bash
# Launch jobfinder to parse jobs, and email recipients

jobfinder
```

### Notifying Recipients

`jobfinder` uses `email` to notify recipients of jobs that have either
closed or opened recently.

In order to do so, `email` needs a useable email address and password,
as well as smtp and port info. This information is stored ina  database tabled
named `jobfinder.db` for SQLite3, and in a Schema named `jobs` in
the default `PostgreSQL` installation.

Access to the SQLite3 Database can be found at the following locations:

```bash
For Windows

C:\Users\%username%\AppData\Local\jobfinder\jobfinder.db

For Linux | MacOSX
$HOME/.local/share/jobfinder/jobfinder.db
```

The data required for the `props` table (SQLite | PostgreSQL) is as follows:

```bash
SMTP=test.server.net
PORT=1234
EMAIL=email@test.net
PASSWORD=password
```

>NOTE: Your password will be in plain text. This is not secure and will
>be addressed in future iterations.** Additionally, `emailer` has only been
>tested with one email and may not work with others.

## Database

The database used for this project (currently) is sqlite. The included
`sqlite.sql` script shows the current database structure.

## Moving Forward

This repository currently only gathers State of Montana IT Jobs. It would be
useful to combine this functionality with jobs gathered from the private
and/or non-profit sector.

Additionally, it will likely be useful at some point to provide a web interface
to display the currently gathered jobs. [This list][] has some potentially
useful apis that could help with this.

[William Lake]: https://github.com/William-Lake/job_finder
[This list]: https://github.com/toddmotto/public-apis#jobs
[jobfinder]: https://github.com/William-Lake/job_finder
[Greg Beam]: https://github.com/KI7MT
[PyPi]: https://test.pypi.org/
[requirements.txt]: https://github.com/William-Lake/job_finder/blob/master/requirements.txt
[central job site]: https://mtstatejobs.taleo.net/careersection/200/jobsearch.ftl?lang=en
[this guide]: https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation
[Job Finder]: https://github.com/William-Lake/job_finder
