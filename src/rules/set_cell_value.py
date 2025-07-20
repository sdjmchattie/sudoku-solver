from model.cell import Cell
from model.grid import Grid


def set_cell_value(grid: Grid, cell: Cell, value: int) -> None:
    """
    Set the value of a cell in the grid and update its neighbours' candidates.

    Args:
        grid (Grid): The Sudoku grid containing the cell.
        cell (Cell): The cell to be updated with a value.
        value (int): The value to set for the cell.
    """
    cell.value = value

    incomplete_neighbours = (
        neighbour for neighbour in grid.get_neighbours(cell) if neighbour.value is None
    )

    for neighbour in incomplete_neighbours:
        neighbour.candidates = neighbour.candidates.difference({cell.value})
