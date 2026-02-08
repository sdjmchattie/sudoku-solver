from model.grid import Grid
from rules.all_rules import apply as apply_rules

class Solver:
    def __init__(self, grid: Grid, use_nishio: bool = True):
        """Construct a Solver instance with the given Sudoku grid.

        Args:
            grid (Grid): The Sudoku grid to be solved.
            use_nishio (bool): Whether to use the Nishio rule as a last resort.
                Defaults to True.
        """
        self.grid = grid
        self.use_nishio = use_nishio

    def solve(self):
        """Solve the Sudoku puzzle using a cycle of rules until no more rules can be applied."""
        while True:
            # If no rules apply, we cannot proceed further
            if not apply_rules(self.grid, self.use_nishio):
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
            if cell.value is None and len(cell.candidates) == 0:
                return False

            if cell.value is not None and any(
                neighbour.value == cell.value
                for neighbour in self.grid.get_neighbours(cell)
            ):
                return False

        return True
