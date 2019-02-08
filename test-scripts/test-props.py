""" Simple script to test SQLite3 props table"""

import os
from os.path import expanduser
import sys

def get_user_home():
    """Return User Home Directory"""
    return expanduser("~")

# Comment / Uncomment the DB paths below based on yoru system

# For Windows
db = get_user_home() + "\AppData\Local\job_finder\jobfinder.db"

# For Linux
# db = get_user_home() + "/.local/share/job_finder/jobfinder.db"

# No edits required beyond this point.
# TODO Using PostGres now, need to use it instead. This can likely be achieved via models.py
# data = {}
# try:
#     conn = sqlite3.connect(db)
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM props WRE ROWID = 1')
#     data = cur.fetchone()
# except sqlite3.OperationalError as sql3_error:
#     print("Failed fetchall on props => {sql3_error}".format(sql3_error=sql3_error))
#     sys.exit(2)

# print("\n")
# print(data)
# print("\n")
# print(data[0])
# print(data[1])
# print(data[2])

sys.exit(0)