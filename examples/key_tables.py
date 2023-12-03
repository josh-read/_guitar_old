import drawsvg as draw
from grid import Grid
from notes import Scale

chromatic_scale = Scale.chromatic()
diatonic_scale = Scale.diatonic()

n_row = len(diatonic_scale) + 1
n_col = len(chromatic_scale) + 1

grid = Grid(x=0, y=0, n_cols=n_col, n_rows=n_row, cell_size=(50, 50))

d = draw.Drawing(grid.grid_width, height=grid.grid_height)

# fill in the top row
top_row_y = grid.row_centres[0]
for e, c, chromatic_note in zip(grid.col_edges[1:], grid.col_centres[1:], chromatic_scale):
    if chromatic_note in diatonic_scale:
        degree = diatonic_scale.semitones.index(chromatic_note.semitone)
        text = draw.Text(str(degree + 1), x=c, y=top_row_y, font_size=12, text_anchor='middle', dominant_baseline='middle')
        d.append(text)
        if degree in (1, 3, 5):
            rect = draw.Rectangle(x=e, y=grid.y, width=grid.cell_width, height=grid.grid_height,
                                  fill='orange', fill_opacity=0.3, stroke='orange')
            d.append(rect)

# draw in rest of table
for offset, (semitone, y) in enumerate(zip(diatonic_scale, grid.row_centres[1:])):
    scale = Scale.chromatic()
    # print(interval_list[semitone:], interval_list[:semitone])
    text = draw.Text(str(offset + 1), x=grid.col_centres[0], y=y, font_size=12, text_anchor='middle', dominant_baseline='middle')
    d.append(text)
    for note, c in zip(scale, grid.col_centres[1:]):
        note.semitone += semitone.semitone
        text = draw.Text(note.interval, x=c, y=y, font_size=12, text_anchor='middle', dominant_baseline='middle')
        d.append(text)

d.save_svg('../drawings/key_table.svg')
