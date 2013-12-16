#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from bitbucket.bitbucket import Bitbucket

parser = argparse.ArgumentParser(description='Fetch data from Bitbucket repo.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                   help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))


def main(args):


if __name__ == "__main__":
    main()