#!/usr/bin/python3
# coding: utf-8

# Written by Manuel Pégourié-Gonnard, 2017. WTFPL v2.

"""Print information about a scale (for now, chosen at random)."""

from scales import Scale


def print_comparison(fingerings):
    """Print possible fingerings with criterion justifying each comparison."""
    print()
    for i in range(len(fingerings) - 1):
        print(fingerings[i], fingerings[i].compare(fingerings[i+1]))
    print(fingerings[-1])


scale = Scale.random()
rh = scale.fingerings(right_hand=True)
lh = scale.fingerings(right_hand=False)
print('{} {} {}'.format(scale, lh[0], rh[0]))

print_comparison(lh)
print_comparison(rh)
