#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import platform
import logging
import sys
import time
import traceback


""" This is a skeleton template I use before writing any magic """

__all__ = ['main']
__author__ = ""
__url__ = ""
__version__ = ""
__license__ = ""


LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'

# Timing decorator
def timing(func):
    def wrapper(*args, **kwargs):
        start = time.clock() if 'Windows' == platform.system() \
            else time.time()
        result = func(*args, **kwargs)
        end = time.clock() if 'Windows' == platform.system() else time.time()
        logging.info("{0} took {1:.3g} ms".format(func.func_name,
                    (end - start) * 1000.0))
        return result
    return wrapper


def init_argparser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-t', '--run-tests', action='store_true',
                        help='run all tests')
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='increase chattiness of script')
    return parser


@timing
def do_work_son(args):
    pass


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = init_argparser()
    args = parser.parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format=LOG_FORMAT)

    try:
        if args.run_tests:
            _test()
        else:
            do_work_son(args)
    except:
        trace = traceback.format_exc()
        logging.error("OMGWTFBBQ: {0}".format(trace))
        sys.exit(1)

    # Yayyy-yah
    sys.exit(0)


def _test():
    """ Do some testing, yo """
    import doctest
    doctest.testmod(sys.modules[__name__])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

# vim: filetype=python
