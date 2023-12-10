from itertools import accumulate

from note import Note
from rotating_list import RotatingList


class Scale(RotatingList):

    def __init__(self, semitones, root_note=None):
        """Initialise with the semitones in the scale. A root note can additionally be set."""
        super().__init__(semitones)
        self.root_note = root_note

    def __iter__(self):
        for semitone in super(Scale, self).__iter__():
            yield Note(semitone)

    def __getitem__(self, item):
        result = super(Scale, self).__getitem__(item)
        return Scale(result, root_note=self.root_note)

    @classmethod
    def chromatic(cls, *args, **kwargs):
        chromatic_semitones = range(13)
        return cls(semitones=chromatic_semitones, *args, **kwargs)

    @classmethod
    def diatonic(cls, *args, mode=0, **kwargs):
        ionian_intervals = [2, 2, 1, 2, 2, 2, 1]
        mode_intervals = ionian_intervals[mode:] + ionian_intervals[:mode]
        mode_semitones = accumulate(mode_intervals, initial=0)
        return cls(semitones=mode_semitones, *args, **kwargs)
