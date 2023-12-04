import drawsvg as draw
from grid import Grid
from itertools import accumulate


latin_names = {
    0: 'C',
    1: 'C#',
    2: 'D',
    3: 'D#',
    4: 'E',
    5: 'F',
    6: 'F#',
    7: 'G',
    8: 'G#',
    9: 'A',
    10: 'A#',
    11: 'B',
}


intervals = {
    0: 'P1',
    1: 'm2',
    2: 'M2',
    3: 'm3',
    4: 'M3',
    5: 'P4',
    6: 'TT',
    7: 'P5',
    8: 'm6',
    9: 'M6',
    10: 'm7',
    11: 'M7',
    12: 'P8'
}


class Scale:

    def __init__(self, semitones, root_note=None):
        """Initialise with the semitones in the scale. A root note can additionally be set."""
        self.semitones = semitones
        self.root_note = root_note
        self.iter_semitones = None

    def __len__(self):
        return len(self.semitones)

    def __iter__(self):
        self.iter_semitones = iter(self.semitones)
        return self

    def __next__(self):
        try:
            semitone = next(self.iter_semitones)
        except StopIteration as e:
            raise e
        return Note(semitone, scale=self)

    @classmethod
    def chromatic(cls, *args, **kwargs):
        chromatic_semitones = range(13)
        return cls(semitones=chromatic_semitones, *args, **kwargs)

    @classmethod
    def diatonic(cls, *args, mode=0, **kwargs):
        ionian_intervals = [2, 2, 1, 2, 2, 2, 1]
        mode_intervals = ionian_intervals[mode:] + ionian_intervals[:mode]
        mode_semitones = list(accumulate(mode_intervals, initial=0))
        return cls(semitones=mode_semitones, *args, **kwargs)


class Note:

    def __init__(self, semitone, scale=None):
        """Get information about the note."""
        self.semitone = semitone
        self.scale = scale

    def __repr__(self):
        return f"Note({self.interval=})"

    def __eq__(self, other):
        if isinstance(other, Note):
            try:
                return self.latin_name == other.latin_name
            except TypeError:
                return self.semitone == other.semitone
        else:
            return self.semitone == other

    @property
    def interval(self):
        return intervals[self.semitone % 12]

    @property
    def latin_name(self):
        if self.scale.root_note is None:
            raise TypeError("Parent scale has no root note.")
        return latin_names[(self.semitone + self.scale.root_note) % 12]


# face color, stroke color
colors = {
    0: ('red', 'black'),
    1: ('black', 'white'),
    2: ('black', 'white'),
    3: ('black', 'white'),
    4: ('black', 'white'),
    5: ('black', 'white'),
    6: ('black', 'white'),
    7: ('black', 'white'),
    8: ('black', 'white'),
    9: ('black', 'white'),
    10: ('black', 'white'),
    11: ('black', 'white'),
    12: ('black', 'white'),
}


def draw_note(drawing, x, y, note):
    face_color, stroke_color = colors[note.semitone % 12]
    circle = draw.Circle(x, y, r=20, fill=face_color, stroke=stroke_color)
    drawing.append(circle)
    text = draw.Text(note.interval, font_size=12, x=x, y=y, text_anchor='middle', dominant_baseline='middle', fill=stroke_color)
    drawing.append(text)


if __name__ == '__main__':
    chromatic_scale = Scale.chromatic()

    grid = Grid(x=0, y=0, n_cols=len(chromatic_scale), n_rows=1, cell_size=(50, 50))
    d = draw.Drawing(width=grid.grid_width, height=grid.grid_height)

    y, = grid.row_centres
    for x, note in zip(grid.col_centres, chromatic_scale):
        draw_note(d, x, y, note)

    d.save_svg('../drawings/notes.svg')
