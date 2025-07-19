from enum import Enum, auto
import re

from model.point import Point

from .cell import Cell

numeric_regex = re.compile(r"^[1-9]$")


class Scope(Enum):
    BLOCK = auto()
    NONE = auto()


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

        grid: set[Cell] = set()
        for irow, row in enumerate(values):
            for icol, value in enumerate(row):
                grid.add(
                    Cell(
                        coord=Point(icol, irow),
                        block=Point(icol // 3, irow // 3),
                        coord_in_block=Point(icol % 3, irow % 3),
                        value=value,
                    )
                )

        self._grid = grid

    def __iter__(self):
        """
        Iterate over the cells in the grid.

        Returns:
            Iterator[Cell]: An iterator over the Cell objects in the grid.
        """
        return iter(self._grid)

    def __getitem__(self, coord: Point) -> Cell | None:
        """
        Get the Cell at the specified Point of the grid.

        Args:
            coord (Point): The coord of the desired cell.

        Returns:
            Cell: The Cell object at the specified coord, or None if the coord does not exist in the grid.
        """
        return next((cell for cell in self._grid if cell.coord == coord), None)

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

    def get_neighbours(self, cell: Cell) -> set[Cell]:
        """
        Get the 20 neighbouring cells of a specified cell in the grid.
        Neighbours include cells in the same row, column, and 3x3 block.

        Args:
            cell (Cell): The cell to find neighbours of.

        Returns:
            set[Cell]: A set of 20 Cell objects that are neighbours to the specified cell.

        Raises:
            ValueError: If the cell does not exist in the grid.
        """
        if cell not in self._grid:
            raise ValueError("Cell does not exist in the grid.")

        return (
            self.get_block_cells(cell.block)
            .union(self.get_column_cells(cell.coord.x))
            .union(self.get_row_cells(cell.coord.y))
            .difference({cell})  # Exclude the cell itself
        )

    def get_block_cells(self, block: Point) -> set[Cell]:
        """
        Get the 9 cells in the 3x3 block with given coordinates.

        Args:
            block (Point): The coordinates of the 3x3 block within the grid.

        Returns:
            set[Cell]: A set of 9 Cell objects in the same 3x3 block, or zero items if the block doesn't exist.
        """
        return {cell for cell in self._grid if cell.block == block}

    def get_column_cells(self, index: int, block_index: int | None = None) -> set[Cell]:
        """
        Get cells in the same column.

        Args:
            index (int): The index of the column to fetch Cells from.
            block_index (int | None): Optional.
              If provided, only Cells in the block with the given row index will be returned.

        Returns:
            set[Cell]: A set of Cell objects in the same column.
              If the column index does not exist, or the block_coord does not exist, an empty set is returned.
        """
        block = Point(index // 3, block_index) if block_index is not None else None

        def predicate(cell: Cell) -> bool:
            return cell.coord.x == index and (block is None or cell.block == block)

        return {cell for cell in self._grid if predicate(cell)}

    def get_row_cells(self, index: int, block_index: int | None = None) -> set[Cell]:
        """
        Get cells in the same row.

        Args:
            index (int): The index of the row to fetch Cells from.
            block_index (int | None): Optional.
              If provided, only Cells in the block with the given column index will be returned.

        Returns:
            set[Cell]: A set of Cell objects in the same row.
              If the row index does not exist, or the block_coord does not exist, an empty set is returned.
        """
        block = Point(block_index, index // 3) if block_index is not None else None

        def predicate(cell: Cell) -> bool:
            return cell.coord.y == index and (block is None or cell.block == block)

        return {cell for cell in self._grid if predicate(cell)}

    def display(self):
        """
        Display the grid in a human-readable format.
        """
        for row_index in range(1, 10):
            if row_index % 3 == 1:
                print("+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+")

            for col_index in range(1, 10):
                if col_index % 3 == 1:
                    print("|", end=" ")

                cell = self[Point(col_index - 1, row_index - 1)]
                print(cell.value or ".", end=" ")

            print("|")

        print("+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+")
