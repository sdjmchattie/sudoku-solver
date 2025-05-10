import re

from .cell import Cell

numeric_regex = re.compile(r"^\d$")


class Grid:
    def __init__(self, values: list[list[int | None]]):
        """
        Initialize the grid with cells for the values.

        Args:
            values (list): A 2D list of integers representing the grid.
        """
        self._create_grid(values)

    def _create_grid(self, values: list[list[int | None]]):
        """
        Create a 2D list of Cell objects from the given values.
        Each value in the list is used to create a Cell object.
        If the value is None, the cell will be initialized with no value.

        Args:
            values (list): A 2D list of integers or None representing the grid.
        """
        grid = []
        for row in values:
            grid_row = []
            for value in row:
                grid_row.append(Cell(value))
            grid.append(grid_row)
        self._grid = grid

    @classmethod
    def from_rows_notation(self, rows: list[str]) -> "Grid":
        """
        Create a 2D list of values from a list of strings, where each string represents a row of the grid.
        """
        values = []
        for row in rows:
            values.append(
                [int(x) if numeric_regex.match(x) else None for x in row.strip()]
            )

        return Grid(values)

    def display(self):
        """
        Display the grid in a human-readable format.
        """
        for row_index, row in enumerate(self._grid):
            if row_index % 3 == 0 and row_index != 0:
                print("-" * 6 + "+" + "-" * 7 + "+" + "-" * 6)

            for col_index, cell in enumerate(row):
                if col_index % 3 == 0 and col_index != 0:
                    print("|", end=" ")

                if cell.value is not None:
                    print(f"{cell.value}", end=" ")
                else:
                    print(".", end=" ")

            print()
