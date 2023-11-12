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

    @property
    def grid_width(self):
        return self.cell_width * self.n_cols

    @property
    def grid_height(self):
        return self.cell_height * self.n_rows
