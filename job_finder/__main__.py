from argparse import ArgumentParser

from job_finder import main


def gather_args():

    arg_parser = ArgumentParser(description='Gathers and notifies recipients about IT jobs at the State of Montana.')

    arg_parser.add_argument(
        '--setup',
        action='store_true',
        help='Creates the database tables and gathers the email properties.'
    )

    arg_parser.add_argument(
        '--add_recip',
        action='store_true',
        help='Whether the following recipients or recipient file should be added to the database.'
    )

    arg_parser.add_argument(
        '--remove_recip',
        action='store_true',
        help='Whether the following recipients or recipient file should be removed from the database.'
    )

    arg_parser.add_argument(
        '--use_recip_file',
        action='store_true',
        help='Whether a file of emails is being provided to the job_finder. NOTE: .txt files only, one email per line.'
    )

    arg_parser.add_argument(
        'recipients',
        nargs='*',
        help='One or more recipient emails, or file(s) containing the emails that should be (added to/removed from) the database.'
    )

    return arg_parser.parse_args()


if __name__ == "__main__":

    # args = gather_args()

    # main(args)

    main(None)
