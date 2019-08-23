#!/usr/bin/python3

# Written by Manuel Pégourié-Gonnard, 2019. WTFPL v2.

"""
Tools for exploring the scales and their fingering at the piano.

Classes:
    - Note: one of the 12 notes.
    - Mode: major or minor (harmonic).
    - ScaleFingering: a fingering of a scale.
    - Scale: a scale, defined by tonic and mode.
"""

import random


class Note:
    """
    One of the 12 notes in the chromatic scale.

    Internally represented by its index, 0 = Do/C.
    """

    # https://en.wikipedia.org/wiki/Musical_note#12-tone_chromatic_scale
    # French
    note_names = ('Do', 'Ré', 'Mi', 'Fa', 'Sol', 'La', 'Si')
    substitutions = {}
    # # English
    # note_names = ('C', 'D', 'E', 'F', 'G', 'A', 'B')
    # substitutions = {}
    # # German
    # note_names = ('C', 'D', 'E', 'F', 'G', 'A', 'H')
    # substitutions = { 'H♭': 'B' }

    # symbols are common to the three supported systems
    sharp_sym = '♯'  # compose-#-#
    flat_sym = '♭'   # compose-#-b

    # white keys on a piano keyboard (aka C major scale)
    white_keys = (0, 2, 4, 5, 7, 9, 11)

    # quick access to names of white keys
    white_names = dict(zip(white_keys, note_names))

    @staticmethod
    def each(stride=1):
        """
        Iterate over notes, chromatically or by a given interval.

        The stride is usually 1 (default) or 7 (circle of fifths).
        The interval must be co-prime with 12 (ie not 2, 3, 4, 6) if you want
        to reach each of the 12 notes.
        """
        return (Note(rank % 12) for rank in range(0, 12 * stride, stride))

    @staticmethod
    def random():
        """Return a note chosen at random."""
        return Note(random.randrange(12))

    def __init__(self, rank):
        """Create a note with the given rank."""
        self.rank = rank

    def is_black(self):
        """Tell if the key corresponding to that note is black on a piano."""
        return self.rank not in self.white_keys

    @classmethod
    def whites_from(cls, from_note):
        """Iterate over white keys from the given starting point."""
        i = cls.white_keys.index(from_note)
        return cls.white_keys[i:] + cls.white_keys[:i]

    def closest_white_keys(self):
        """Find the white keys (unaltered notes) closest from self."""
        prv = -1
        for cur in self.white_keys:
            if cur == self.rank:
                return (cur, )
            if cur > self.rank:
                return (prv, cur)
            prv = cur

    def name_with_base_white(self, base_white):
        """Return our name by adding alterations to the given base."""
        base_name = self.white_names[base_white]

        distance = (self.rank - base_white) % 12
        if distance >= 6:
            distance -= 12

        if distance > 0:
            alter = self.sharp_sym * distance
        elif distance < 0:
            alter = self.flat_sym * abs(distance)
        else:
            alter = ''

        full_name = base_name + alter

        # support for "B" in the German system
        if full_name in self.substitutions:
            full_name = self.substitutions[full_name]

        return full_name

    def __str__(self):
        """Return string represention, prefering unaltered and sharps."""
        return self.name_with_base_white(self.closest_white_keys()[0])

    def __add__(self, half_steps):
        """Return the note a given number of half-steps above ourselves."""
        new_rank = (self.rank + half_steps) % 12
        return Note(new_rank)


class Mode:
    """One of the common modes: for now, major and minor harmonic."""

    # mode names
    # French
    names = ('Majeur', 'Mineur')
    # # English
    # names = ('Major', 'Minor')
    # # German
    # names = ('dur', 'moll')

    # modes represented by number of half-steps between successive notes
    intervals_list = (
        (2, 2, 1, 2, 2, 2, 1),  # major
        (2, 1, 2, 2, 1, 3, 1),  # minor harmonic
    )

    @classmethod
    def each(cls):
        """Iterate over all available modes."""
        return (Mode(i) for i in range(len(cls.intervals_list)))

    @classmethod
    def random(cls):
        """Return a mode chosen at random."""
        return Mode(random.randrange(len(cls.intervals_list)))

    def __init__(self, index):
        """Create a mode given by its index: 0 = Major, 1 = Minor harmonic."""
        self.intervals = self.intervals_list[index]
        self.name = self.names[index]
        self.index = index

    def __str__(self):
        """Return the name of the mode."""
        return self.name


class ScaleThumbMap:
    """Map of where the thumb can, should and should not go in a scale.

    The main member of interest is scores which is a 8-tuple of pairs:
    - boolean indicating whether the thumb goes there in C Major
    - convenience score for placing the thumb here.

    Other members are:
    - symmetry: used to unite left and right hand (see __init__)
    - notes: the notes with this symmetry applied
    """

    c_major_thumb = (True, False, False, True, False, False, False, True)

    def __init__(self, scale_8_notes, *, right_hand):
        """Create a map for the given notes and hand."""
        # For left hand, internally work with descending fingering
        # in order to unify with right hand:
        # - reverse the notes internally;
        # - reverse the fingers when printing.
        #
        # (That's the reason we want 8 notes in the scale.)
        self.symmetry = (lambda l: l) if right_hand else (lambda l: l[::-1])
        self.notes = self.symmetry(scale_8_notes)

        self.scores = []
        for i in range(8):
            note = self.notes[i]
            prev = self.notes[i-1]
            self.scores.append(self.score(note, prev))

        # pack convenience score with whether the thumb goes there in C major
        self.scores = tuple(zip(self.c_major_thumb, self.scores))

    @staticmethod
    def score(note, prev):
        """Return a thumb convenience score for the given pair of notes.

        Scoring is as follows:
        -2 forbidden (black key)
        -1 inconvenient (passing on augmented second)
        0 neutral
        1 convenient (passing after black key)
        """
        if note.is_black():
            return -2

        dist = abs(note.rank - prev.rank)
        if dist > 6:
            dist = 12 - dist
        if dist > 2:
            return -1

        if prev.is_black():
            return 1

        return 0


class ScaleFingering:
    """A fingering for a 7-notes scale."""

    base = (1, 2, 3, 1, 2, 3, 4)

    def __init__(self, thumb_map, i):
        """Create a fingering for the given thumb convenience map and index.

        The thumb convenience map is a ScaleThumbMap object.

        The index is used to rotate the basic fingering 1231234 into one of
        the 7 possible fingerings that follow the same pattern.
        """
        self.map = thumb_map

        # set up fingers by rotating "base" (C major) fingering
        # and extending to 8 notes
        self.fingers = self.base[i:] + self.base[:i]
        self.fingers += (5 if self.fingers[-1] == 4 else self.fingers[0], )

        # extract thumb score for our thumb positions
        finger_scores = zip(self.fingers, thumb_map.scores)
        self.thumb_scores = tuple(s for f, s in finger_scores if f == 1)

    def __str__(self):
        """Return fingering as a string of 8 digits."""
        return ''.join(self.map.symmetry(tuple(str(f) for f in self.fingers)))

    @staticmethod
    def each(thumb_map):
        """Iterate over all fingerings for a scale given by it thumbs map."""
        return (ScaleFingering(thumb_map, i) for i in range(7))

    def is_acceptable(self):
        """Return False if that fingering puts the thumb on a black key."""
        return not any(s[1] == -2 for s in self.thumb_scores)

    def ends_with_pinky(self):
        """Return True if this is the familiar C Major fingering."""
        return all(s[0] for s in self.thumb_scores)

    def starts_with_thumb(self):
        """Return True if this fingering puts the thumb on the tonic."""
        return self.fingers[0] == 1

    def has_no_long_passing(self):
        """Return False on thumb-passings on interval larger than a second."""
        return not any(s[1] == -1 for s in self.thumb_scores)

    def nb_black_passings(self):
        """Return the number of times passing the thumb after a black key."""
        return sum(1 for s in self.thumb_scores if s[1] == 1)

    def compare(self, other):
        """Compare to another fingering and return preference code and reason.

        The preference code is:
            - +1 if self is better than other,
            - 0 if they have equal preference,
            - -1 otherwise.

        The reason (str) represents the differentiating criterion.
        """
        # this function was designed to prefer the standard fingering
        # for each of the 24 major and minor (harmonic) scales for both hands
        #
        # we use the following list of desirable criteria:
        criteria = (
                ('ends_with_pinky',     +1),
                ('starts_with_thumb',   +1),
                ('has_no_long_passing', +1),
                ('nb_black_passings',   +1),
        )

        for name, desirability in criteria:
            s = getattr(self, name)()
            o = getattr(other, name)()

            comp = ((s > o) - (s < o)) * desirability
            if comp != 0:
                return comp, name

        return 0, ''

    def __lt__(self, other):
        """Return True if self is preferred to other."""
        # define "less than" as "preferred" so that sorting
        # puts the preferred fingerings first without reversing
        return self.compare(other)[0] > 0

    def is_group1(self):
        """Return True if this is the standard C Major fingering."""
        return self.ends_with_pinky()

    def is_group2(self):
        """Return True if the 4th finger is on the same key as in F♯ Major."""
        fourth_position = self.fingers.index(4)
        fourth_note = self.map.notes[fourth_position]
        fourth_note_wanted = self.map.symmetry((10, 6))[0]
        return fourth_note.rank == fourth_note_wanted

    def is_group3(self):
        """Return True is this is neither group 1 or 2."""
        return not (self.is_group1() or self.is_group2())

    def groups(self):
        """Return a tuple of groups this fingering belongs to."""
        groups = tuple()
        if self.is_group1():
            groups += (1,)
        if self.is_group2():
            groups += (2,)
        if self.is_group3():
            groups += (3,)
        return groups


class Scale:
    """A 7-notes scale defined by tonic and mode."""

    def __init__(self, tonic, mode):
        """Create scale based on tonic (Note) and mode (Mode)."""
        self.tonic = tonic
        self.mode = mode

        # set up 8 notes - tonic on both ends
        # this makes left hand descending symmetric to right hand ascending
        # by having both start and end with the tonic
        notes = [tonic]
        for i in mode.intervals:
            notes.append(notes[-1] + i)
        self.notes = tuple(notes)

        # compute thumb convenience maps for each hand
        self.maps = dict(
                (right_hand, ScaleThumbMap(self.notes, right_hand=right_hand))
                for right_hand in (False, True)
        )

    @staticmethod
    def each(circle_of_fifths=True):
        """Iterate over all scales, by circle of fifths of chromatically.

        Circle of fifths starts with: C Major, A Minor, G Major, E Minor, etc.
        Chromatic starts with: C Major, C Minor, D♭ Major, C♯ Minor, etc.
        """
        if not circle_of_fifths:
            return (Scale(note, mode)
                    for note in Note.each()
                    for mode in Mode.each())

        return (Scale((note + (-3) if i else note), mode)
                for note in Note.each(7)
                for i, mode in enumerate(Mode.each()))

    @staticmethod
    def random():
        """Return a scale chosen at random."""
        return Scale(Note.random(), Mode.random())

    @staticmethod
    def all_random():
        """Return a randomly shuffled list of all scales."""
        scales = list(Scale.each(False))
        random.shuffle(scales)
        return scales

    def spellings(self):
        """Return a one or two-element list of 7-tuples with note names.

        Choose the spelling with no double-sharps or double-flats, and the
        least number of sharps/flats in the note names, and return both in
        case of equality.
        """
        scale_candidates = []
        nb_alt_prev = 7
        for tonic_base in self.tonic.closest_white_keys():
            note_names = []
            bad = False
            nb_alt = 0
            for i, cur_base in enumerate(Note.whites_from(tonic_base)):
                cur_note = self.notes[i]
                name = cur_note.name_with_base_white(cur_base)
                note_names.append(name)

                if Note.sharp_sym in name or Note.flat_sym in name:
                    nb_alt += 1
                if Note.sharp_sym * 2 in name or Note.flat_sym * 2 in name:
                    bad = True

            if not bad:
                if nb_alt < nb_alt_prev:
                    scale_candidates = []
                scale_candidates.append(tuple(note_names))
                nb_alt_prev = nb_alt

        return scale_candidates

    def __str__(self):
        """Return the name of the scale (tonic + mode) as a string."""
        return self.spellings()[0][0] + ' ' + str(self.mode)

    def fingerings(self, *, right_hand):
        """Return a tuple of acceptable fingers with most preferred first."""
        fs = ScaleFingering.each(self.maps[right_hand])
        return tuple(sorted(f for f in fs if f.is_acceptable()))

    def thumb_scores(self, *, right_hand):
        """Return a tuple of thumb scores associated with each note.

        Each score is a pair of:
        - does the thumb goes here in C Major? (boolean)
        - numerical convenience score from -2 to 1, see ScaleThumbMap.score.
        """
        m = self.maps[right_hand]
        return m.symmetry(m.scores)
