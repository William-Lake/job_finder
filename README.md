# Job Finder

| Application Data ||
| ---| --- |
| Package            | [jobfinder][]
| Version            | 0.1.4
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

* Python >= 3.5
* OS - Tested on:
    * Ubuntu 18.04
    * Windows 10
* Postgresql Database (Written with 11)
    * (Ubuntu Install)[https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04]
    * (Windows Install)[https://www.postgresql.org/download/windows/]

## Installation

>NOTE: This process is to be used during development. When the package is ready
> for General Availability to the public, a standard `pip install <package-name>`
> will be used rather than the `-e .` convention. Likewise, there will be no
> need to clone the repository beforehand.

### Python

* Language
    * (https://www.python.org/downloads/windows/)[Windows Installer]
    * (https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-18-04-quickstart)[Ubuntu Install]
* Virtual Environment (Optional)
    * (VirtualEnv)[https://virtualenv.pypa.io/en/latest/]
    * (Anaconda)[https://www.anaconda.com/]
    * (Miniconda)[https://docs.conda.io/en/latest/miniconda.html]
* Dependencies
    * All the required modules are outlined in requirements.txt file, and can be installed via pip:

`pip install -r requirements.txt`

### Database

* If you haven't already, download and install Postgresql.
    * (Ubuntu Install)[https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04]
    * (Windows Install)[https://www.postgresql.org/download/windows/]
* Once installed, you'll need to perform some minor database setup. The required changes are outlined in the script job_finder\resources\postgres.sql which can be ran to implement the changes.
    * E.g. `sudo -u postgres psql < job_finder/resources/postgres.sql`
    * TODO: Need the equivalent command and/or instructions for Windows.

### Initial Setup

Before it can be used JobFinder needs to create its tables and gather some info needed for sending emails. The process can be started by using the `--setup` flag:

`python job_finder --setup`

You will be prompted for the smtp, port, email, and password.

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

Adding recipients is performed via the --add_recip flag:

```bash
python job_finder --add_recip test_recip@gmail.com list_of_recips.txt second_recip@mail.com
```

Notice that both email addresses and .txt files can be provided. The order doesn't matter, they can be intermixed. However, the text files must contain one email per line.

### Remove Recipient

Removing recipients is performed via the `--remove_recip` flag:

```bash
python job_finder --remove_recip test_recip@gmail.com list_of_recips.txt second_recip@mail.com
```

Notice that both email addresses and .txt files can be provided. The order doesn't matter, they can be intermixed. However, the text files must contain one email per line.

### Gather Jobs

To perform the default `Job_Finder` functions, you would execute the `jobfinder`
script with no arguments:

```bash
# Launch jobfinder to parse jobs, and email recipients

python jobfinder
```

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
