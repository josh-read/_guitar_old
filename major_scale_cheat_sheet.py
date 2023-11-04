import drawsvg as draw
import numpy as np

intervals_ = {
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

major_scale = [0, 2, 4, 5, 7, 9, 11, 12]
minor_scale = [0, 2, 3, 5, 7, 8, 10, 12]

n_strings = 17
n_frets = 17

string_interval = 5  # for an instrument tuned to 5ths

xx, yy = np.mgrid[0:n_strings, 0:n_frets]
notes = (xx-1) + string_interval * (yy-1)
intervals = notes % 12
print(intervals)

width = 500
string_locations = np.linspace(0, width, n_strings)[1:-1]

height = 1000
fret_locations = np.linspace(0, height, n_frets+1)[1:-1]
fret_centres = fret_locations[:-1] + (fret_locations[1] - fret_locations[0]) / 2

d = draw.Drawing(width, height, origin='top-left')

# Draw an irregular polygon
for x in string_locations:
    ymin, ymax = fret_locations[[0, -1]]
    line = draw.Lines(x, ymin,
                      x, ymax,
                      stroke='black')
    d.append(line)

for y in fret_locations:
    xmin, xmax = string_locations[[0, -1]]
    line = draw.Lines(xmin, y,
                      xmax, y,
                      stroke='black')
    d.append(line)

for interval_row, y in zip(intervals, fret_centres):
    for interval, x in zip(interval_row, string_locations):
        if interval not in major_scale:
            continue
        fill_color = 'red' if interval == 0 else 'black'
        text_color = 'black' if interval == 0 else 'white'
        d.append(draw.Circle(x, y, 10,
                fill=fill_color, stroke_width=2, stroke='black'))
        text = intervals_[interval]
        d.append(draw.Text(text, 12, x, y, fill=text_color, text_anchor='middle', dominant_baseline='middle'))

d.save_svg('drawings/major_scale.svg')
