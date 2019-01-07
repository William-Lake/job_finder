import os
import sys

from os.path import expanduser

SMTP = 'test.server.net'
PORT = '1234'
EMAIL = 'email@test.net'
PASSWORD = 'password'

def get_user_home():
    """Return User Home Directory"""
    return expanduser("~")

def get_db():
    """Get AppData Directory based on Platform"""
    if sys.platform == 'win32':
        DB_NAME = os.path.abspath(os.path.join(
            get_user_home(),'AppData','local','job_finder','Helena_Jobs.db')) 
    else:
        DB_NAME = os.path.abspath(os.path.join(
            get_user_home(),'.local','share','job_finder','Helena_Jobs.db')) 

    return DB_NAME
