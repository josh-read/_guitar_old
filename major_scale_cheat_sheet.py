import drawsvg as draw
import numpy as np
from collections.abc import Iterable
from itertools import accumulate


class Fretboard:

    def __init__(self, *, n_frets: int, string_intervals: (int | Iterable), n_strings: int = None,
                 note_offset=0):
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


class FretboardDrawing(draw.Drawing):

    def __init__(self, fretboard, *args, **kwargs):
        self.fretboard = fretboard
        super(FretboardDrawing, self).__init__(*args, **kwargs)
        self.string_locations = np.linspace(0, self.width, len(self.fretboard.string_notes))[1:-1]
        self.fret_locations = np.linspace(0, self.height, self.fretboard.n_frets + 1)[1:-1]
        self.fret_centres = self.fret_locations[:-1] + (self.fret_locations[1] - self.fret_locations[0]) / 2
        self.draw_fretboard()

    def draw_fretboard(self):
        # draw strings
        for x in self.string_locations:
            ymin, ymax = self.fret_locations[[0, -1]]
            line = draw.Lines(x, ymin,
                              x, ymax,
                              stroke='black')
            self.append(line)
        # draw frets
        for y in self.fret_locations:
            xmin, xmax = self.string_locations[[0, -1]]
            line = draw.Lines(xmin, y,
                              xmax, y,
                              stroke='black')
            self.append(line)

    def draw_notes(self, note_filter: list, note_map: dict):
        for interval_row, y in zip(self.fretboard.notes, self.fret_centres):
            for interval, x in zip(interval_row, self.string_locations):
                if interval not in note_filter:
                    continue
                fill_color = 'red' if interval == 0 else 'black'
                text_color = 'black' if interval == 0 else 'white'
                self.append(draw.Circle(x, y, 10,
                                           fill=fill_color, stroke_width=2, stroke='black'))
                text = note_map[interval]
                self.append(
                    draw.Text(text, 12, x, y, fill=text_color, text_anchor='middle', dominant_baseline='middle'))


def test_fretboard_init():
    assert isinstance(Fretboard(n_frets=12, string_intervals=[5, 5, 5, 4, 5]), Fretboard)
    assert isinstance(Fretboard(n_frets=12, string_intervals=5, n_strings=6), Fretboard)


if __name__ == '__main__':
    intervals = {
        0: 'R',
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
        12: 'Oct'
    }

    scales = {
        'major': [0, 2, 4, 5, 7, 9, 11, 12],
        'pentatonic': [0, 2, 4, 7, 9],
    }

    # draw major and pentatonic scales on large grid
    for name, scale in scales.items():
        fb = Fretboard(n_frets=17, n_strings=17, string_intervals=5, note_offset=6)
        fbd = FretboardDrawing(fb, width=500, height=1000)
        fbd.draw_notes(scale, intervals)
        fbd.save_svg(f'drawings/{name}_scale.svg')
