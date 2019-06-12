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
parser.add_argument('-n', '--notes',
                    help='print note names instead of fingerings',
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


def reason(fingerings):
    """Return the reason why the standard fingering is preferred"""
    if len(fingerings) == 1:
        return '(single)'

    return fingerings[0].compare(fingerings[1])[1]


for scale in Scale.each(not args.chromatic):
    if scale.mode.index not in allowed_modes[args.modes]:
        continue

    if args.notes:
        spellings = (' '.join(notes) for notes in scale.spellings())
        print(scale, '-', ' / '.join(spellings))
    else:
        print(str(scale).ljust(10), end='')

        want_left, want_right = allowed_hands[args.hands]
        if want_left:
            lh = scale.fingerings(right_hand=False)
            print('', lh[0], end='')
        if want_right:
            rh = scale.fingerings(right_hand=True)
            print('', rh[0], end='')

        if args.explain:
            if want_left:
                print('', reason(lh), end='')
            if want_right:
                print('', reason(rh), end='')

        print()
