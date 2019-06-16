#!/usr/bin/python3
# coding: utf-8

# Written by Manuel Pégourié-Gonnard, 2019. WTFPL v2.

"""Print groups of scales that share the same fingering."""

import argparse

from scales import Scale

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-m', '--modes',
                    help='print scales in this/these mode(s)',
                    choices=('major', 'minor', 'both'),
                    default='both',
                    action='store')
parser.add_argument('-H', '--hands',
                    help='print fingerings for this/these hand(s)',
                    choices=('left', 'right', 'both'),
                    default='both',
                    action='store')
args = parser.parse_args()

allowed_modes = {
        'major': (0, ),
        'minor': (1, ),
        'both': (0, 1),
}

allowed_hands = {
        'left': (True, False),
        'right': (False, True),
        'both': (True, True),
}

groups = dict()
for scale in Scale.each():
    if scale.mode.index not in allowed_modes[args.modes]:
        continue

    index = tuple()
    want_left, want_right = allowed_hands[args.hands]
    if want_left:
        index += (str(scale.fingerings(right_hand=False)[0]), )
    if want_right:
        index += (str(scale.fingerings(right_hand=True)[0]), )

    if index not in groups:
        groups[index] = list()
    groups[index].append(scale)

for index, scales in groups.items():
    print(' '.join(index), '-', ' '.join(str(s) for s in scales))
