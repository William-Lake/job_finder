# -*- coding: utf-8 -*-
# Copyright (C) 2018 William Lake
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
"""
Job

Represents an IT Job found in Helena, MT.

"""


class Job(object):

    def __init__(self, job_id, site_id, contest_num, title, dept, site_url):
        """Constructor
        
        Arguments:
            job_data {list} -- The list of job data to use when building this job object.
        """

        self.job_id = job_id

        self.site_id = site_id

        self.contest_num = contest_num

        self.title = title

        self.dept = dept

        self.site_url = site_url
