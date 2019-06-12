#!/usr/bin/python3

# Written by Manuel Pégourié-Gonnard, 2019. WTFPL v2.

import secrets


class Note:
    """
    One of the 12 notes in the chromatic scale.
    Internally represented by its index, 0 = Do/C
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
        return (Note(rank % 12) for rank in range(0, 12 * stride, stride))

    @staticmethod
    def random():
        return Note(secrets.randbelow(12))

    def __init__(self, rank):
        self.rank = rank

    def is_black(self):
        return self.rank not in self.white_keys

    @classmethod
    def whites_from(cls, from_note):
        i = cls.white_keys.index(from_note)
        return cls.white_keys[i:] + cls.white_keys[:i]

    def closest_white_keys(self):
        prv = -1
        for cur in self.white_keys:
            if cur == self.rank:
                return (cur, )
            if cur > self.rank:
                return (prv, cur)
            prv = cur

    def name_with_base_white(self, base_white):
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
        return self.name_with_base_white(self.closest_white_keys()[0])

    def __add__(self, half_steps):
        new_rank = (self.rank + half_steps) % 12
        return Note(new_rank)


class Mode:
    """
    One of the common modes: for now, major and minor harmonic
    """

    # mode names
    # French
    names = ('Majeur', 'Mineur')
    # # English
    # names = ('Major', 'Minor')

    # modes represented by number of half-steps between successive notes
    intervals_list = (
        (2, 2, 1, 2, 2, 2, 1),  # major
        (2, 1, 2, 2, 1, 3, 1),  # minor harmonic
    )

    @classmethod
    def each(cls):
        return (Mode(i) for i in range(len(cls.intervals_list)))

    @classmethod
    def random(cls):
        return Mode(secrets.randbelow(len(cls.intervals_list)))

    def __init__(self, index):
        self.intervals = self.intervals_list[index]
        self.name = self.names[index]

    def __str__(self):
        return self.name


class ScaleFingering:
    """A fingering for a 7-notes scale"""

    base = (1, 2, 3, 1, 2, 3, 4)

    def __init__(self, scale_8_notes, i, *, right_hand):
        # For left hand, internally work with descending fingering
        # in order to unify with right hand:
        # - reverse the notes internally;
        # - reverse the fingers when printing.
        #
        # (That's the reason we want 8 notes in the scale.)
        self.symmetry = (lambda l: l) if right_hand else (lambda l: l[::-1])
        self.notes = self.symmetry(scale_8_notes)

        # set up fingers by rotating "base" (C major) fingering
        # and extending to 8 notes
        self.fingers = self.base[i:] + self.base[:i]
        self.fingers += (5 if self.fingers[-1] == 4 else self.fingers[0], )

    def __str__(self):
        return ''.join(self.symmetry(tuple(str(f) for f in self.fingers)))

    @staticmethod
    def each(scale_8_notes, *, right_hand):
        return (ScaleFingering(scale_8_notes, i, right_hand=right_hand)
                for i in range(7))

    def is_acceptable(self):
        """Fingerings that put the thumb on a black key are not acceptable"""
        for note, finger in zip(self.notes, self.fingers):
            if finger == 1 and note.is_black():
                return False
        return True

    def ends_with_pinky(self):
        """Is this the familiar C major fingering?"""
        return self.fingers[-1] == 5

    def starts_with_thumb(self):
        """Do we start the scale with the thumb?"""
        return self.fingers[0] == 1

    def has_long_passing(self):
        """Do we have thumb passing on intervals larger than a second?
        (This is inconvenient, and can only happen in minor scales.)"""
        for i in range(7):
            dist = abs(self.notes[i].rank - self.notes[i-1].rank)
            if dist > 6:
                dist = 12 - dist
            if dist > 2 and self.fingers[i] == 1:
                return True
        return False

    def nb_black_passings(self):
        """Number of times passing the thumb after a black key
        (which is convenient as it leaves more room underneath)"""
        black_passings = 0
        for i in range(7):
            if self.fingers[i] == 1 and self.notes[i-1].is_black():
                black_passings += 1
        return black_passings

    def compare(self, other):
        """Return (pref, reason) where pref is:
        +1 if self is better than other,
        0 if they have equal preference,
        -1 otherwise
        and reason is a string representing the criterion used to
        differentiate them"""

        # this function was designed to prefer the standard fingering
        # for each of the 24 major and minor (harmonic) scales for both hands
        #
        # we use the following list of (un)desirable criteria:
        criteria = (
                ('ends_with_pinky',     +1),
                ('starts_with_thumb',   +1),
                ('has_long_passing',    -1),
                ('nb_black_passings',   +1),
        )

        for name, desirability in criteria:
            s = getattr(self, name)()
            o = getattr(other, name)()

            cmp = ((s > o) - (s < o)) * desirability
            if cmp != 0:
                return cmp, name

        return 0, ''

    def __lt__(self, other):
        # define "less than" as "preferred" so that sorting
        # puts the preferred fingerings first without reversing
        return self.compare(other)[0] > 0


class Scale:
    """A 7-notes scale defined by tonic and mode"""

    def __init__(self, tonic, mode):
        self.tonic = tonic
        self.mode = mode

        # set up 8 notes - tonic on both ends
        # this makes left hand descending symmetric to right hand ascending
        # by having both start and end with the tonic
        notes = [tonic]
        for i in mode.intervals:
            notes.append(notes[-1] + i)
        self.notes = tuple(notes)

    @staticmethod
    def each(circle_of_fifths=True):
        if not circle_of_fifths:
            return (Scale(note, mode)
                    for note in Note.each()
                    for mode in Mode.each())

        return (Scale((note + (-3) if i else note), mode)
                for note in Note.each(7)
                for i, mode in enumerate(Mode.each()))

    @staticmethod
    def random():
        return Scale(Note.random(), Mode.random())

    def spellings(self):
        """A one or two-element list of 7-tuples with note names.

        Choose the spelling with no double-sharps or double-flats, and the
        least number of sharps/flats in the note names, and return both in
        case of equality."""
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
        return self.spellings()[0][0] + ' ' + str(self.mode)

    def fingerings(self, *, right_hand):
        fs = ScaleFingering.each(self.notes, right_hand=right_hand)
        return tuple(sorted(f for f in fs if f.is_acceptable()))


if __name__ == '__main__':
    # select a random scale and print its fingering (for daily practice)
    scale = Scale.random()
    rh = scale.fingerings(right_hand=True)[0]
    lh = scale.fingerings(right_hand=False)[0]
    print('{} {} {}'.format(scale, rh, lh))

    # # print standard fingering of all LH minor scales by circle of fifths
    # for note in Note.each(7):
    #     scale = Scale(note + (-3), Mode(1))
    #     lh = scale.fingerings(right_hand=False)[0]
    #     print('{: <10} {}'.format(str(scale), lh))

    # # print standard fingering for each scale+hand with deciding criterion
    # for scale in Scale.each():
    #     name = str(scale).ljust(10)
    #     for hand_name, right in (('RH', True), ('LH', False)):
    #         fingerings = scale.fingerings(right_hand=right)
    #         best = fingerings[0]
    #         if len(fingerings) == 1:
    #             reason = '(single)'
    #         else:
    #             reason = best.compare(fingerings[1])[1]
    #         print(name, hand_name, best, len(fingerings), reason)

    # # explore all options for a specific scale and hand
    # scale = Scale(Note(5), Mode(0))
    # print(scale)
    # fs = scale.fingerings(right_hand=True)
    # for i in range(len(fs) - 1):
    #     print(fs[i], fs[i].compare(fs[i+1]))
    # print(fs[-1])

    # # group scales by fingering
    # groups = dict()
    # for scale in Scale.each(True):
    #     rh = str(scale.fingerings(right_hand=True)[0])
    #     lh = str(scale.fingerings(right_hand=False)[0])
    #     index = (rh, lh)
    #     if index not in groups:
    #         groups[index] = list()
    #     groups[index].append(scale)
    # for (rh, lh), scales in groups.items():
    #     print(rh, lh, ' '.join(str(s) for s in scales))
