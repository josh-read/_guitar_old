import drawsvg as draw
from grid import Grid

from scale import Scale

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
    12: 'C',
}


interval_names = {
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


class Note(int):

    def __new__(cls, semitone, scale=None):
        """Get information about the note."""
        instance = super(Note, cls).__new__(cls, semitone)
        instance.scale = scale
        return instance

    def __repr__(self):
        self_as_int = str(int(self))
        description = f'semitone={self_as_int}'

        try:
            description += f', interval={self.interval}'
        except KeyError:
            pass

        try:
            description += f', latin_name={self.latin_name}'
        except TypeError:
            pass

        return f"Note({description})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        try:
            return self.latin_name == other.latin_name
        except TypeError:
            return super(Note, self).__eq__(other)

    def __hash__(self):
        return super(Note, self).__hash__()

    @property
    def interval(self):
        return interval_names[self]

    @property
    def latin_name(self):
        try:
            return latin_names[(self + self.scale.root_note) % 12]
        except AttributeError:
            raise TypeError("Parent scale has no root note.")


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
    12: ('red', 'black'),
}


def draw_note(drawing, x, y, note):
    face_color, stroke_color = colors[note]
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
