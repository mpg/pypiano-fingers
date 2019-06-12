#!/usr/bin/python3
# coding: utf-8

# Written by Manuel Pégourié-Gonnard, 2019. WTFPL v2.

"""
Print all scales with their standard fingering
"""

import argparse

from scales import Scale

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--chromatic',
                    help='sort chromatically rather than by circle-of-fifths',
                    action='store_true')
args = parser.parse_args()

for scale in Scale.each(not args.chromatic):
    rh = scale.fingerings(right_hand=True)[0]
    lh = scale.fingerings(right_hand=False)[0]
    print('{: <10} {} {}'.format(str(scale), rh, lh))
