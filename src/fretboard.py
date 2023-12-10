from itertools import accumulate
from typing import Iterable


class Fretboard:

    def __init__(self, *, n_frets: int, string_intervals: (int | Iterable), n_strings: int = None,
                 note_offset=0):
        """Fretboard provides a model of a fretboard. The intervals between strings can be specified manually,
        in which case the number of strings is inferred from the number of intervals. Alternatively, where the intervals
        between strings are equal, a single value for string_intervals is accepted provided n_strings is also specified."""
        self.n_frets = n_frets
        if isinstance(string_intervals, Iterable):
            self.string_intervals = string_intervals
        elif isinstance(string_intervals, int) and isinstance(n_strings, int):
            self.string_intervals = [string_intervals] * (n_strings - 1)
        else:
            raise TypeError()

        self.string_notes = list(accumulate([-note_offset] + self.string_intervals))
        # calculate note number - note number cycles after 12 semitones
        self.notes = [[(string + fret) % 12 for string in self.string_notes] for fret in range(n_frets)]
