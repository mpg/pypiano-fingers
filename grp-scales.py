#!/usr/bin/python3
# coding: utf-8

# Written by Manuel Pégourié-Gonnard, 2019. WTFPL v2.

"""Print groups of scales that share similar fingerings."""

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
criterion = parser.add_mutually_exclusive_group()
criterion.add_argument('-4', '--fourth',
                       help='sort by 4-th finger note (rather than fingering)',
                       action='store_true')
criterion.add_argument('-p', '--predefined',
                       help='sort by pre-defined groups: 1. C Major fingering;\
                       2. fingers on the same notes as in F# Major; 3. other',
                       action='store_true')
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


def hand_index(scale, *, right_hand):
    """Compute index (fingering, 4th finger note, or groups) for this hand."""
    fingering = scale.fingerings(right_hand=right_hand)[0]

    if args.fourth:
        fourth_position = str(fingering).index('4')
        fourth_note = scale.notes[fourth_position]
        return str(fourth_note)

    if args.predefined:
        return 'g' + ''.join(str(g) for g in fingering.groups())

    return str(fingering)


groups = dict()
for scale in Scale.each():
    if scale.mode.index not in allowed_modes[args.modes]:
        continue

    index = tuple()
    want_left, want_right = allowed_hands[args.hands]
    if want_left:
        index += (hand_index(scale, right_hand=False), )
    if want_right:
        index += (hand_index(scale, right_hand=True), )

    if index not in groups:
        groups[index] = list()
    groups[index].append(scale)

for index, scales in groups.items():
    print(' '.join(index), '-', ', '.join(str(s) for s in scales))
