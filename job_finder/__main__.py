from argparse import ArgumentParser
import logging
import os

from job_finder import main

DEFAULT_CONFIG_FILE = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)), 'logging.conf')


def setup_logging(config_file=DEFAULT_CONFIG_FILE):
    """
    Loads logging configuration from the given configuration file.

    Code from: https://github.com/storj/storj-python-sdk/blob/master/tests/log_config.py

    Code found via: https://www.programcreek.com/python/example/105587/logging.config.fileConfig

    :param config_file:
        the configuration file (default=/etc/package/logging.conf)
    :type config_file: str
    """

    # TODO: Figure out why the logging file wasn't loading

    logging.basicConfig(level=logging.DEBUG)

    # if (
    #     not os.path.exists(config_file) or
    #         not os.path.isfile(config_file)):

    #     msg = '%s configuration file does not exist!', config_file

    #     logging.getLogger().error(msg)

    #     raise ValueError(msg)

    # try:
    #     fileConfig(config_file, disable_existing_loggers=False)

    #     logging.getLogger().info('%s configuration file was loaded.',
    #                              config_file)

    # except Exception as e:

    #     logging.getLogger().error('Failed to load configuration from %s!',
    #                               config_file)

    #     logging.getLogger().debug(str(e), exc_info=True)

    #     raise e

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
        'recipients',
        nargs='*',
        help='One or more recipient emails, or file(s) containing the emails that should be (added to/removed from) the database.'
    )

    return arg_parser.parse_args()


if __name__ == "__main__":

    setup_logging()

    args = gather_args()

    main(args)