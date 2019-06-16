Pypiano-fingers
===============

This is just me having fun exploring some piano fingering stuff with Python.

It started when I wanted to understand the standard fingering for scales. A
number of sources explain they're based on two principles: alternating
123/1234 groups, and not putting the thumb on black keys. For several scales,
these principles are not enough to uniquely determine the standard fingering,
so I decided to explore what additional principles can be used for that
purpose in a programmatic way.

Contents
--------

There is one module: `scales.py` with the basic building blocks.

There are three scripts using it to provide a command-line interface for
common operations:

- `all-scales.py` for basic information about each scale
- `grp-scales.py` for listing groups of scales that share identical fingerings
- `one-scale.py` for detailed information about a single scale (by default chosen at
  random, which can be used for daily practice).

Then there's a very minimal test script `t.sh` and supporting data files
`ref-*`. I'm just making sure that when I modify the sorting logic, it still
finds the standard fingering for each scale.

Language
--------

By default, note and mode names are printed in French, as this is my native
language and while I can read note names in the English and German system I
always need to mentally convert them to French names. If your ingrained naming
system differs, the code can easily be adapted to the English and German
systems, just look for `French` in `scales.py` and do the obvious edits.

Use
---

As I said, this is just me having fun, so it's not made for the purpose of
being usable by other people, but if you happen to share some of my interests,
maybe you'll find ways to have fun with this as well!

Happy hacking!
