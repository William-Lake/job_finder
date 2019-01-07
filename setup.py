# -*- coding: utf-8 -*-
# Copyright (C) 2019 William Lake, Greg Beam
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#-------------------------------------------------------------------------------
# Developer Notes:
#
#  package_data allows access to package resources outside the MANIFEST.in
#  listing.  
#  
#  Use pkgutil for accessing jobs/resources/*.*
# 
#  Usage: pkgutil.get_data(package, resource)
#
#  Example:
# 
#  import pkgutil
#  data = pkgutil.get_data("jobfinder", "resources/logging.conf")
#  sql1  = pkgutil.get_data("jobfinder", "resources/sqlite.sql")
#  sql2  = pkgutil.get_data("jobfinder", "resources/postgresql.sql")
#
#  Additional resource vars can be added as needed.
#
#  See Also: https://docs.python.org/3.7/library/pkgutil.html
#
#-------------------------------------------------------------------------------
import os
import setuptools

import jobfinder

here = os.path.dirname(os.path.abspath(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=jobfinder.__title__,
    version=jobfinder.__version__,
    author=jobfinder.__author__,
    license=jobfinder.__license__,
    author_email=jobfinder.__email__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires='>=3.5.*',
    project_urls={
        'Packaging tutorial': 'https://packaging.python.org/tutorials/distributing-packages/',
        'job Finder source': 'https://github.com/KI7MT/job_finder',
},
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'lxml',
        'psycopg2',
    ],
    package_data={
        'jobfinder': [
            'resources/*.sql',
            'resources/*.csv',
            'reources/*.conf',
        ]
    },
    entry_points={
    'console_scripts': ['jobfinder = jobfinder.commands.Driver:Driver'],
    },
    zip_safe=False,
    classifiers=[
        "Natural Language :: English",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Information Technology",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        ],
    url='https://github.com/KI7MT/job_finder',
)