import drawsvg as draw
import numpy as np

from fretboard import Fretboard
from grid import Grid
from units import intervals, scales, notes


class FretboardDrawing(draw.Drawing):

    def __init__(self, fretboard, *args, cell_size=(25, 50), pad=15, **kwargs):
        self.fretboard = fretboard
        n_cols, n_rows = len(fretboard.string_notes)-1, fretboard.n_frets
        self.grid = Grid(pad, pad, n_cols, n_rows, cell_size)
        drawing_width = self.grid.grid_width + 2 * pad
        drawing_height = self.grid.grid_height + 2 * pad
        super(FretboardDrawing, self).__init__(drawing_width, drawing_height, *args, **kwargs)
        self.string_locations = self.grid.col_edges
        self.fret_locations = self.grid.row_edges
        self.fret_centres = self.grid.row_centres
        self.draw_fretboard()

    def draw_fretboard(self):
        # draw strings
        ymin, ymax = self.fret_locations[0], self.fret_locations[-1]
        for x in self.string_locations:
            line = draw.Lines(x, ymin,
                              x, ymax,
                              stroke='black')
            self.append(line)
        # draw frets
        xmin, xmax = self.string_locations[0], self.string_locations[-1]
        for y in self.fret_locations:
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

    # standard fretboard
    for note_offset, note_name in notes.items():
        for scale_name, scale_degrees in scales.items():
            fb = Fretboard(n_frets=13, string_intervals=[5, 5, 5, 4, 5], note_offset=(8 + note_offset))
            fbd = FretboardDrawing(fb)
            fbd.draw_notes(scale_degrees, intervals)
            fbd.save_svg(f'drawings/scales/{scale_name}/{note_name}.svg')

    # draw major and pentatonic scales on large grid
    for scale_name, scale in scales.items():
        fb = Fretboard(n_frets=15, n_strings=15, string_intervals=5, note_offset=6)
        fbd = FretboardDrawing(fb)
        fbd.draw_notes(scale, intervals)
        fbd.save_svg(f'drawings/scales/{scale_name}_large_fretboard.svg')
