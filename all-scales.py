#!/usr/bin/python3
# coding: utf-8

# Written by Manuel Pégourié-Gonnard, 2019. WTFPL v2.

"""
Print all scales with their standard fingering.
"""

import argparse

from scales import Scale

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-c', '--chromatic',
                    help='sort chromatically rather than by circle-of-fifths',
                    action='store_true')
parser.add_argument('-e', '--explain',
                    help='explain why those fingerings were chosen',
                    action='store_true')
parser.add_argument('-n', '--notes',
                    help='print note names instead of fingerings',
                    action='store_true')
args = parser.parse_args()


def reason(fingerings):
    """Return the reason why the standard fingering is preferred"""
    if len(fingerings) == 1:
        return '(single)'

    return fingerings[0].compare(fingerings[1])[1]


for scale in Scale.each(not args.chromatic):
    if args.notes:
        spellings = (' '.join(notes) for notes in scale.spellings())
        print(scale, '-', ' / '.join(spellings))
    else:
        rh = scale.fingerings(right_hand=True)
        lh = scale.fingerings(right_hand=False)
        print('{: <10} {} {}'.format(str(scale), lh[0], rh[0]), end='')
        if args.explain:
            print('', reason(lh), reason(rh), end='')
        print()
