#!/usr/bin/python3
# coding: utf-8

# Written by Manuel Pégourié-Gonnard, 2017. WTFPL v2.

"""Print information about a scale (given by its index or chosen at random)."""

import argparse

# colorama brings windows compat, but that's optional
try:
    import colorama
except ImportError:
    colorama = None

from scales import Scale, Note, Mode

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('index',
                    help='0 = C Major, 1 = C Minor, 2 = D♭ Major...',
                    action='store', type=int,
                    nargs='?', default=None)
parser.add_argument('-a', '--all',
                    help='show all acceptable fingerings',
                    action='store_true')
parser.add_argument('-l', '--legend',
                    help='show a legend of colors and criteria',
                    action='store_true')
args = parser.parse_args()


if colorama:
    RED = colorama.Fore.RED
    YELLOW = colorama.Fore.YELLOW
    WHITE = colorama.Fore.WHITE
    GREEN = colorama.Fore.GREEN
    BRIGHT = colorama.Style.BRIGHT
    NORMAL = colorama.Style.NORMAL
    RESET = colorama.Style.RESET_ALL
else:
    RED = '\x1b[31m'
    YELLOW = '\x1b[33m'
    WHITE = '\x1b[37m'
    GREEN = '\x1b[32m'
    BRIGHT = '\x1b[1m'
    NORMAL = '\x1b[21m'
    RESET = '\x1b[0m'


code_std_pos = {
        True: BRIGHT,
        False: NORMAL,
}
code_score = {
        -2: RED,
        -1: YELLOW,
        0: WHITE,
        1: GREEN,
}


def color(name, std_pos, score, width):
    """Apply color-coding to note name."""
    return (code_std_pos[std_pos] +
            code_score[score] +
            name.ljust(width) +
            RESET)


def pad(fingering, width):
    """Return fingering as a string, each note padded to the given width."""
    return ''.join(str(f).ljust(width) for f in str(fingering))


if args.index:
    scale = Scale(Note(args.index // 2), Mode(args.index % 2))
else:
    scale = Scale.random()

print(scale)

note_names = scale.spellings()[0]
note_names += (note_names[0], )  # make it 8 notes

for right_hand in (False, True):
    fingerings = scale.fingerings(right_hand=right_hand)
    fingering = fingerings[0]
    thumb_map = scale.thumb_scores(right_hand=right_hand)
    annotated = zip(note_names, thumb_map)
    colored = (color(n, sp, sc, 5) for n, (sp, sc) in annotated)
    print()
    print(''.join(colored))
    print(pad(fingering, 5), end='')

    if args.all:
        for i in range(1, len(fingerings)):
            print(fingerings[i-1].compare(fingerings[i])[1])
            print(pad(fingerings[i], 5), end='')
        if len(fingerings) == 1:
            print('(single)', end='')

    print()


def show(style, text):
    """Show description text in the corresponding style."""
    print(style + text + RESET)


if args.legend:
    print()
    print("Color/brightness legend:")
    show(RED, "Never put thumb here (black key)")
    show(YELLOW, "Avoid putting thumb here (passing on augmented second)")
    show(WHITE, "Can put thumb here (white key)")
    show(GREEN, "Prefer putting thumb here (passing after black key)")
    show(BRIGHT + WHITE, "Thumb goes there in C Major fingering (preferred)")

if args.legend and args.all:
    print()
    print("Sorting criteria (why is this fingering preferred to the next?):")
    print("(single): this is the only fingering with no thumb on black keys")
    print("ends_with_pinky: this is the standard C Major fingering")
    print("starts_with_thumb: has thumb on tonic")
    print("has_no_long_passing: avoids passing thumb on augmented second")
    print("nb_black_passings: passes thumb after black key more often")
    print("(nothing): can't decide between this and the next fingering")
