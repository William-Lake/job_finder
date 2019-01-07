# TODO: Create Class to handle prop additions to database via ConfigParser
#       or database tables CRUD entries.

DATABASE="jobfinder.db"
SMTP='test.server.net'
PORT='1234'
EMAIL='email@test.net'
PASSWORD='password'
DATABASE="jobfinder.db"

# Methods used for testing only. Remove after Class for props is setup properly
def get_db_name():
    return DATABASE

def get_smtp():
    return SMTP

def get_port():
    return PORT

def get_email():
    return EMAIL

def get_password():
    return PASSWORD

# END job_finder_props