from model.grid import Grid
from rules import (
    apply_hidden_single_rule,
    apply_hidden_pairs_rule,
    apply_hidden_triples_rule,
    apply_naked_pairs_rule,
    apply_naked_triples_rule,
    apply_single_candidate_rule,
)


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
            # Apply rules, stopping after the first successful application.
            # This ensures we always apply the simplest rules first.
            # This can help with efficiency where complex rules take more CPU cycles to apply.
            applied = (
                apply_single_candidate_rule(self.grid)
                or apply_naked_pairs_rule(self.grid)
                or apply_naked_triples_rule(self.grid)
                or apply_hidden_single_rule(self.grid)
                or apply_hidden_pairs_rule(self.grid)
                or apply_hidden_triples_rule(self.grid)
            )

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
