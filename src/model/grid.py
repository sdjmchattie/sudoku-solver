class Grid:
    def __init__(self, rows):
        pass

    @classmethod
    def from_rows_notation(self, rows):
        """
        Create a grid from a list of strings, where each string represents a row of the grid.
        """
        grid = []
        for row in rows:
            grid.append([int(x) if x != '.' else None for x in row.strip()])

        return Grid(grid)
