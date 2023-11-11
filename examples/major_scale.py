from units import intervals, notes, scales
import drawsvg as draw
from itertools import cycle, islice, count


class Grid:

    def __init__(self, x, y, n_cols, n_rows, cell_size):
        self.x = x
        self.y = y
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.cell_width, self.cell_height = cell_size

    @property
    def col_edges(self):
        return [n * self.cell_width + self.x for n in range(self.n_cols + 1)]

    @property
    def col_centres(self):
        return [(n + 0.5) * self.cell_width + self.x for n in range(self.n_cols)]

    @property
    def row_edges(self):
        return [n * self.cell_height + self.y for n in range(self.n_rows + 1)]

    @property
    def row_centres(self):
        return [(n + 0.5) * self.cell_height + self.y for n in range(self.n_rows)]


width = 400
height = 400


d = draw.Drawing(width+100, height, origin='top-left')

major_scale = scales['major']
counter = count(1)
notes_generator = cycle(notes.values())


n_cols = len(notes) + 1

cell_text_array = (
        [[str(next(counter)) if i in major_scale else '' for i in intervals.keys()]]
        + [list(intervals.keys())]
        + [list(intervals.values())]
        + [list(islice(notes_generator, n_cols)) for _ in range(len(notes))]  # notes
)

n_rows = len(cell_text_array)

col_width = width / n_cols
row_height = height / n_rows

grid = Grid(100, 0, n_cols, n_rows, (col_width, row_height))


for y, row_text in zip(grid.row_centres, cell_text_array):
    for x, cell_text in zip(grid.col_centres, row_text):

        circle = draw.Circle(x, y, 10)
        d.append(circle)

        text = draw.Text(str(cell_text), 12, x=x, y=y, fill='white', text_anchor='middle', dominant_baseline='middle')
        d.append(text)

left_text = ['scale degrees', 'semitones', 'intervals'] + list(islice(notes_generator, len(notes)))

x = grid.col_edges[0] - 10
for y, row_text in zip(grid.row_centres, left_text):
    text = draw.Text(row_text, 12, x=x, y=y, fill='black', text_anchor='end', dominant_baseline='middle')
    d.append(text)

d.save_svg('../drawings/major_scale_table.svg')
