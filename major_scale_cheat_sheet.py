import drawsvg as draw
import numpy as np


class Fretboard:

    def __init__(self, n_strings: int, n_frets: int, string_intervals: int):
        self.n_strings = n_strings
        self.n_frets = n_frets
        self.string_intervals = string_intervals

        xx, yy = np.mgrid[0:self.n_strings, 0:self.n_frets]
        self.notes = ((xx - 1) + self.string_intervals * (yy - 1)) % 12


class FretboardDrawing(draw.Drawing):

    def __init__(self, fretboard, *args, **kwargs):
        self.fretboard = fretboard
        super(FretboardDrawing, self).__init__(*args, **kwargs)
        self.string_locations = np.linspace(0, self.width, self.fretboard.n_strings)[1:-1]
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
        fb = Fretboard(17, 17, 5)
        fbd = FretboardDrawing(fb, width=500, height=1000)
        fbd.draw_notes(scale, intervals)
        fbd.save_svg(f'drawings/{name}_scale.svg')
