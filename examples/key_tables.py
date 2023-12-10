import drawsvg as draw
from grid import Grid
from notes import Scale, draw_note

chromatic_scale = Scale.chromatic()[:-1]
diatonic_scale = Scale.diatonic()[:-1]

n_row = len(diatonic_scale) + 1
n_col = len(chromatic_scale) + 1

grid = Grid(x=0, y=0, n_cols=n_col, n_rows=n_row, cell_size=(50, 50))

d = draw.Drawing(grid.grid_width, height=grid.grid_height)

# draw top row of table
top_row_centre = grid.row_centres[0]
for col_edge, col_centre, chromatic_note in zip(grid.col_edges[1:], grid.col_centres[1:], chromatic_scale):
    if chromatic_note in diatonic_scale:
        scale_degree = 1 + diatonic_scale.index(chromatic_note)
        if scale_degree in (1, 3, 5):
            rect = draw.Rectangle(x=col_edge, y=grid.y, width=grid.cell_width, height=grid.grid_height,
                                  fill='orange', fill_opacity=0.3, stroke='orange')
            d.append(rect)
        text = draw.Text(str(scale_degree), x=col_centre, y=top_row_centre, font_size=12, text_anchor='middle', dominant_baseline='middle')
        d.append(text)


# draw in rest of table
for scale_degree, (diatonic_note, y) in enumerate(zip(diatonic_scale, grid.row_centres[1:]), start=1):
    # draw scale degree in first column
    text = draw.Text(str(scale_degree), x=grid.col_centres[0], y=y, font_size=12, text_anchor='middle', dominant_baseline='middle')
    d.append(text)
    # draw rotated chromatic scale
    chromatic_scale.rotation = diatonic_note
    for note, col_centre in zip(chromatic_scale, grid.col_centres[1:]):
        draw_note(drawing=d, x=col_centre, y=y, note=note)
    chromatic_scale.rotate()


d.save_svg('../drawings/key_table.svg')
