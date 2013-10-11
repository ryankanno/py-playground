#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import cProfile
import functools
import platform
import pstats
import logging
import StringIO
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


def profile(sortby='cumulative'):
    def _inner(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            pr = cProfile.Profile()
            pr.enable()
            retval = pr.runcall(func, *args, **kwargs)
            pr.disable()
            s = StringIO.StringIO()
            pstats.Stats(pr, stream=s).sort_stats(sortby).print_stats()
            print s.getvalue()
            return retval
        return _wrapper
    return _inner


def init_argparser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-t', '--run-tests', action='store_true',
                        help='run all tests')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase chattiness of script')
    return parser


@profile()
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
