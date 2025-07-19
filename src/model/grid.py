import re

from .cell import Cell

numeric_regex = re.compile(r"^[1-9]$")


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
        if len(values) != 9 or any(len(row) != 9 for row in values):
            raise ValueError("Grid must be 9x9.")

        grid: list[list[Cell]] = []
        for row in values:
            grid_row = []
            for value in row:
                grid_row.append(Cell(value))
            grid.append(grid_row)
        self._grid = grid

    def __iter__(self):
        """
        Iterate over the Cells of the grid.

        Returns:
            iterator: An iterator over the Cells of the grid.
                The iterator yields tuples of (row_index, column_index, Cell).
        """
        return (
            (irow, icol, cell)
            for irow, row in enumerate(self._grid)
            for icol, cell in enumerate(row)
        )

    def __getitem__(self, item: tuple[int, int]) -> Cell:
        """
        Get the Cell at the specified row and column indices.

        Args:
            item (tuple[int, int]): A tuple containing the row and column indices.

        Returns:
            Cell: The Cell object at the specified indices.
        """
        row, col = item
        self._validate_index(row, col)

        return self._grid[row][col]

    @classmethod
    def from_rows_notation(self, rows: list[str]) -> "Grid":
        """
        Create a 2D list of values from a list of strings, where each string represents a row of the grid.
        Each character in the string is treated as a cell value.
        If the character is a digit, it is converted to an integer representing a solved value.
        If the character is not a digit, it is treated as an empty cell value.

        Args:
            rows (list): A list of strings representing the rows of the grid.
        """
        values = []
        for row in rows:
            values.append(
                [int(x) if numeric_regex.match(x) else None for x in row.strip()]
            )

        return Grid(values)

    def _validate_index(self, row: int, col: int):
        """
        Validate the row and column indices to ensure they are within the grid bounds.

        Args:
            row (int): The row index.
            col (int): The column index.

        Raises:
            IndexError: If the row or column index is out of bounds.
        """
        if not (0 <= row < 9 and 0 <= col < 9):
            raise IndexError("Row and column indices must be between 0 and 8.")

    def get_neighbours(self, row: int, col: int) -> set[Cell]:
        """
        Get the 20 neighbouring cells of a specified cell in the grid.
        Neighbours include cells in the same row, column, and 3x3 block.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            set[Cell]: A set of 20 Cell objects that are neighbours to the specified cell.
        """
        self._validate_index(row, col)

        return (
            self.get_block_neighbours(row, col)
            .union(self.get_col_neighbours(row, col))
            .union(self.get_row_neighbours(row, col))
        )

    def get_block_neighbours(self, row: int, col: int) -> set[Cell]:
        """
        Get the 8 neighbouring cells in the same 3x3 block as the specified cell.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            set[Cell]: A set of 8 Cell objects in the same 3x3 block.
        """
        self._validate_index(row, col)

        block_row_start = (row // 3) * 3
        block_col_start = (col // 3) * 3
        neighbours = set()

        for r in range(block_row_start, block_row_start + 3):
            for c in range(block_col_start, block_col_start + 3):
                if r != row or c != col:
                    neighbours.add(self[r, c])

        return neighbours

    def get_col_neighbours(self, row: int, col: int) -> set[Cell]:
        """
        Get the 8 neighbouring cells in the same column.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            set[Cell]: A set of 8 Cell objects in the same column.
        """
        self._validate_index(row, col)

        return {self[irow, col] for irow in range(9) if irow != row}

    def get_row_neighbours(self, row: int, col: int) -> set[Cell]:
        """
        Get the 8 neighbouring cells in the same row.

        Args:
            row (int): The row index of the cell.

        Returns:
            set[Cell]: A set of 8 Cell objects in the same row.
        """
        self._validate_index(row, col)

        return {cell for icol, cell in enumerate(self._grid[row]) if icol != col}

    def display(self):
        """
        Display the grid in a human-readable format.
        """
        for row_index, row in enumerate(self._grid):
            if row_index % 3 == 0:
                print("+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+")

            for col_index, cell in enumerate(row):
                if col_index % 3 == 0:
                    print("|", end=" ")

                print(cell.value or ".", end=" ")

            print("|")

        print("+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+")
