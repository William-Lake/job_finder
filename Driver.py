"""Driver class, manages the job_finder utility."""


import sys
import os
from datetime import datetime
from job_finder import job_finder

def gather_arguments():
    """Gathers the command line arguments if they exist."""

    print('Gathering Command Line Arguments')

    arguments = []

    try:

        arguments.append(sys.argv[1])

        arguments.append(sys.argv[2])

    except:

        arguments = None

    return arguments

def print_banner():

    current_dir = os.path.dirname(os.path.abspath(__file__))

    banner = open(os.path.join(current_dir,'job_finder_banner.txt')).read()

    current_date = datetime.now().strftime('%c')

    print(banner)

    print(current_date)

def execute_job_finder(jf,arguments=None):
    """Executes the Job Finder module.
    
    Arguments:
        jf {job_finder} -- The Job Finder object.
    
    Keyword Arguments:
        arguments {list} -- The list of command line arguments provided. (default: {None})
    """
    print('Starting Job Finder')

    try:

        if arguments != None:

            parse_arguments(jf,arguments)

        else:
        
            jf.gather_and_review_jobs()

    except Exception as err: 

        print('There was an error during job_finder execution: ')

        print(err)

def parse_arguments(jf,arguments):
    """Parses the provided command line arguments.
    
    Arguments:
        jf {job_finder} -- The Job Finder object.
        arguments {list} -- The command line arguments to parse.
    """
    print('Parsing Command Line Arguments')

    target = arguments[1].strip()

    if arguments[0].upper() == 'ADD':

        if target.endswith('.txt'): jf.add_recipients(target)

        else: jf.add_recipient(target)

    elif arguments[0].upper() == 'REMOVE':

        if target.endswith('.txt'): jf.remove_recipients(target)
        
        else: jf.remove_recipient(target)

arguments = gather_arguments()

print_banner()

jf = job_finder()

execute_job_finder(jf,arguments)

if jf.conn_closed == False: jf.dbu.close_connection()

print('\n\n+----------------------------------------------------------------+\n\n')