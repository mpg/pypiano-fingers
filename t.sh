#!/bin/sh

set -eu

# general source quality checks
flake8 *.py

# compare computed fingering to reference
./all-scales.py     > my-scales-harmonic
./all-scales.py -c  > my-scales-chromatic
diff {my,ref}-scales-harmonic
diff {my,ref}-scales-chromatic
rm my-scales-{harmonic,chromatic}
