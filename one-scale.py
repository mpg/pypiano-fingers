#!/usr/bin/python3
# coding: utf-8

# Written by Manuel Pégourié-Gonnard, 2017. WTFPL v2.

"""Print information about a scale (given by its index or chosen at random)."""

import argparse

from scales import Scale, Note, Mode

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('index',
                    help='0 = C Major, 1 = C Minor, 2 = D♭ Major...',
                    action='store', type=int,
                    nargs='?', default=None)
args = parser.parse_args()


def print_comparison(fingerings):
    """Print possible fingerings with criterion justifying each comparison."""
    print()
    for i in range(len(fingerings) - 1):
        print(fingerings[i], fingerings[i].compare(fingerings[i+1]))
    print(fingerings[-1])


if args.index:
    scale = Scale(Note(args.index // 2), Mode(args.index % 2))
else:
    scale = Scale.random()

rh = scale.fingerings(right_hand=True)
lh = scale.fingerings(right_hand=False)
print('{} {} {}'.format(scale, lh[0], rh[0]))

print_comparison(lh)
print_comparison(rh)
