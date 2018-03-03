"""Driver class, manages the job_finder utility."""


import sys
from job_finder import job_finder

def gather_arguments():
    """Gathers the command line arguments if they exist."""

    arguments = []

    try:

        arguments.append(sys.argv[1])

        arguments.append(sys.argv[2])

    except:

        arguments = None

    return arguments

def execute_job_finder(jf,arguments=None):
    """Executes the Job Finder module.
    
    Arguments:
        jf {job_finder} -- The Job Finder object.
    
    Keyword Arguments:
        arguments {list} -- The list of command line arguments provided. (default: {None})
    """

    # Attempt to execute job finder...
    try:

        if arguments != None:

            parse_arguments(jf,arguments)

        else:
        
            jf.gather_and_review_jobs()

    except: # ...but if there were issues, make sure the db connection is closed.

        print('There was an error during job_finder execution.')

        if jf.conn_closed == False: 
            
            jf.dbu.close_connection()

def parse_arguments(jf,arguments):
    """Parses the provided command line arguments.
    
    Arguments:
        jf {job_finder} -- The Job Finder object.
        arguments {list} -- The command line arguments to parse.
    """

    email = arguments[1]

    if arguments[0].upper() == 'ADD':

        jf.add_recipient(email)

    elif arguments[0].upper() == 'REMOVE':

        jf.remove_recipient(email)

jf = job_finder()

arguments = gather_arguments()

execute_job_finder(jf,arguments)