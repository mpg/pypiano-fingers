#!/bin/sh

set -eu

./all-scales.py | sed 's/  *[1-5].*//' | sort > all-sorted

for hand in left right; do
    ./grp-scales.py --hand=$hand |
        sed -n '/Do Majeur/s/^.* - //p' |
        sed 's/, /,/g' | tr ',' '\n' > g1-$hand

    ./grp-scales.py -4 --hand=$hand |
        sed -n '/Fa♯ Majeur/s/^.* - //p' |
        sed 's/, /,/g' | tr ',' '\n' > g2-$hand

    sort -u g1-$hand g2-$hand > sofar-sorted
    diff all-sorted sofar-sorted | sed -n 's/< //p' > g3-$hand
done

rm sofar-sorted all-sorted
