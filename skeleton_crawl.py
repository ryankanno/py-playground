#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import cProfile
import functools
import logging
import os
import pstats
import string
import StringIO
import sys
import traceback

# I love this to abstract out httplib, urllib, etc complexities
import mechanize

""" This module is just a template I use before performing crawling magic """

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
    parser.add_argument('url', help='url to crawl')
    parser.add_argument('-d', '--directory', default=os.getcwd(),
                        help='directory to store crawl')
    parser.add_argument('-t', '--run-tests', action='store_true',
                        help='run all tests')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase chattiness of script')
    return parser


def create_filename(fname):
    valid_chars = "-_.() {0}{1}".format(string.ascii_letters, string.digits)
    return ''.join(c for c in fname if c in valid_chars)


def get_browser():
    """ Set policies, user agents, proxies, behaviors, etc. in here """
    return mechanize.Browser()


def crawl_url(browser, url):
    logging.debug("Crawling {0}".format(url))
    response = browser.open(url)
    return response.read()


def save_crawl(path_to_file, response):
    logging.debug("Saving to: {0}".format(path_to_file))

    dirname = os.path.dirname(path_to_file)

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(path_to_file, "wb") as f:
        f.write(response)


def do_crawl_son(args):
    brow = get_browser()
    resp = crawl_url(brow, args.url)
    save_crawl(os.path.join(args.directory, create_filename(args.url)), resp)


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
            do_crawl_son(args)
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
