#!/usr/bin/python3
# coding: utf-8

# Written by Manuel Pégourié-Gonnard, 2017. WTFPL v2.

"""
Print information about a scale (for now, chosen at random)
"""

from scales import Scale


def print_comparison(fingerings):
    print()
    for i in range(len(fingerings) - 1):
        print(fingerings[i], fingerings[i].compare(fingerings[i+1]))
    print(fingerings[-1])


scale = Scale.random()
rh = scale.fingerings(right_hand=True)
lh = scale.fingerings(right_hand=False)
print('{} {} {}'.format(scale, rh[0], lh[0]))

print_comparison(rh)
print_comparison(lh)
