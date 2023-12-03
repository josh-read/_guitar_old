import drawsvg as draw

from units import intervals, scales
from grid import Grid
from itertools import count


major_scale = scales['major']
scale_degrees = [v for k, v in intervals.items() if k in major_scale]
interval_list = list(intervals.values())

n_cols = len(intervals) + 1
n_rows = len(major_scale) + 1

# initialise grid and drawing
grid = Grid(0, 0, n_cols, n_rows, cell_size=(25, 25))
d = draw.Drawing(width=grid.grid_width, height=grid.grid_height)

# draw headings in first row
first_row_y = grid.row_centres[0]
counter = count(start=1)
for i, (c, l) in enumerate(zip(grid.col_centres, grid.col_edges), start=0):
    if i-1 in major_scale:
        n = next(counter)
        text = draw.Text(str(n), x=c, y=first_row_y, font_size=12, text_anchor='middle', dominant_baseline='middle')
        d.append(text)
        if n in (1, 3, 5):
            rect = draw.Rectangle(x=l, y=grid.y, width=grid.cell_width, height=grid.grid_height,
                                  fill='orange', fill_opacity=0.3, stroke='orange')
            d.append(rect)

# draw in rest of table
for scale_degree, (semitone, y) in enumerate(zip(major_scale, grid.row_centres[1:])):
    row = interval_list[semitone:] + interval_list[:semitone]
    # print(interval_list[semitone:], interval_list[:semitone])
    text = draw.Text(str(scale_degree + 1), x=grid.col_centres[0], y=y, font_size=12, text_anchor='middle', dominant_baseline='middle')
    d.append(text)
    for interval, c in zip(row, grid.col_centres[1:]):
        text = draw.Text(interval, x=c, y=y, font_size=12, text_anchor='middle', dominant_baseline='middle')
        d.append(text)

d.save_svg('../drawings/key_table.svg')
