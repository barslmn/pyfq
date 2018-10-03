#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'bars'

import sys
import argparse
from argparse import RawTextHelpFormatter
from pyfq.core import catfq
from pyfq import __version__
from importlib import util

mpl_exists = util.find_spec('matplotlib') is not None

if mpl_exists:
    from pyfq.core import qcfq


def get_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='tool')

    parser.add_argument('--version',
                        action='version', version=__version__)

    parser_catfq = subparsers.add_parser(
        'CAT',
        formatter_class=RawTextHelpFormatter,
        help='Cat fastq files in given directory',
        epilog='''Usage examples:
        pyfq CAT
        pyfq CAT -i /path/to/fastqs -o /path/to/output
        ''')

    parser_catfq.add_argument('-i', '--input', required=False,
                              default='./', type=str,
                              help='Directory of fastq(.gz)s to cat.')
    parser_catfq.add_argument('-o', '--output', required=False,
                              default='./', type=str,
                              help='Directory to write catted fastq(.gz)(s)')

    parser_qcfq = subparsers.add_parser(
        'QC',
        formatter_class=RawTextHelpFormatter,
        help='Create quality reports for given fastqs',
        epilog='''Usage examples:
        pyfq QC 
        pyfq QC -i /path/to/fastq -o /path/to/output -f html
        ''')
    parser_qcfq.add_argument('-i', '--input', required=True,
                             default=None, type=str,
                             help='Directory of fastq(.gz)s')
    parser_qcfq.add_argument('-o', '--output', required=True,
                             default=None, type=str,
                             help='Output directory')
    parser_qcfq.add_argument('-f', '--output-format', required=False,
                             default='html', type=str, help='Output format')

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    main(args)


def main():
    args = get_args()
    if args.tool == 'CAT':
        catfq.main(args)
    if args.tool == 'QC':
        if mpl_exists:
            qcfq.main(args)
        else:
            sys.write.stderr('matplotlib is required.')
