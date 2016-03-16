#! /usr/bin/env python
from __future__ import print_function
import sys
import os


import os
import argparse
import sys
sys.path.append(
    os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..")))
from mykrobe.version import __version__
import logging

from base import ArgumentParserWithDefaults
from base import DEFAULT_KMER_SIZE
from mykatlas import sequence_parser_mixin

def run_subtool(parser, args):
    if args.command == "predict":
        from mykrobe.cmds.amr import run

    # run the chosen submodule.
    run(parser, args)


def main():
    #########################################
    # create the top-level parser
    #########################################
    parser = argparse.ArgumentParser(
        prog='mykrobe',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--version", help="mykrobe version",
                        action="version",
                        version="%(prog)s " + str(__version__))
    subparsers = parser.add_subparsers(
        title='[sub-commands]',
        dest='command',
        parser_class=ArgumentParserWithDefaults)


    #########################################
    # create the individual tool parsers
    #########################################

    # ##########
    # # AMR predict
    # ##########

    parser_amr = subparsers.add_parser(
        'predict',
        parents=[sequence_parser_mixin],
        help="predict the sample's antibiogram")
    parser_amr.add_argument(
        'species',
        metavar='species',
        choices=['staph', 'tb'],
        type=str,
        help='species')
    parser_amr.add_argument(
        '--panel',
        metavar='panel',
        type=str,
        help='variant panel (default:bradley-2015)',
        choices=['bradley-2015', 'walker-2015'],
        default='bradley-2015')

    parser_amr.add_argument('--force', default=False, action="store_true")
    parser_amr.set_defaults(func=run_subtool)



    args = parser.parse_args()
    args.func(parser, args)


if __name__ == "__main__":
    main()