#!/usr/bin/python3
# coding: utf-8

# Written by Manuel Pégourié-Gonnard, 2017. WTFPL v2.

"""Print information about a scale (given by its index or chosen at random)."""

import argparse

from colorama import Fore, Style

from scales import Scale, Note, Mode

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('index',
                    help='0 = C Major, 1 = C Minor, 2 = D♭ Major...',
                    action='store', type=int,
                    nargs='?', default=None)
args = parser.parse_args()

code_std_pos = {
        True: Style.BRIGHT,
        False: Style.NORMAL,
}
code_score = {
        -2: Fore.RED,
        -1: Fore.YELLOW,
        0: Fore.WHITE,
        1: Fore.GREEN,
}


def color(name, std_pos, score):
    """Apply color-coding to note name."""
    return (code_std_pos[std_pos] +
            code_score[score] +
            name.ljust(4) +
            Style.RESET_ALL)


if args.index:
    scale = Scale(Note(args.index // 2), Mode(args.index % 2))
else:
    scale = Scale.random()

print(scale)

note_names = scale.spellings()[0]
note_names += (note_names[0], )  # make it 8 notes

for right_hand in (False, True):
    thumb_map = scale.thumb_scores(right_hand=right_hand)
    fingering = scale.fingerings(right_hand=right_hand)[0]
    annotated = zip(note_names, thumb_map)
    colored = (color(n, sp, sc) for n, (sp, sc) in annotated)
    print()
    print(''.join(colored))
    print(''.join(str(f).ljust(4) for f in str(fingering)))
