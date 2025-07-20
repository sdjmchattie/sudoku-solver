from model.grid import Grid
from rules import solve_single_candidates


class Solver:
    def __init__(self, grid: Grid):
        """Construct a Solver instance with the given Sudoku grid.

        Args:
            grid (Grid): The Sudoku grid to be solved.
        """
        self.grid = grid

    def solve(self):
        """Solve the Sudoku puzzle using a cycle of rules until no more rules can be applied."""
        while True:
            applied = False

            # Apply rules
            applied |= solve_single_candidates(self.grid)

            # If no rules were applied, we cannot proceed further
            if not applied:
                break

    def is_solved(self) -> bool:
        """Check whether the Sudoku grid is completely solved.

        Returns:
            bool: True if all cells have values, False otherwise.
        """
        return all(cell.value is not None for cell in self.grid)

    def is_valid(self) -> bool:
        """Check if the current grid state is valid.
        Valid means that all cells with values do not conflict with their neighbours.

        Returns:
            bool: True if all solved cells do not conflict with their neighbours.
        """
        for cell in self.grid:
            if cell.value is not None and any(
                neighbour.value == cell.value
                for neighbour in self.grid.get_neighbours(cell)
            ):
                return False

        return True
