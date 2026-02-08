from model.grid import Grid
from rules.set_cell_value import set_cell_value
from solver import Solver


def apply_nishio_rule(grid: Grid) -> bool:
    """Apply the Nishio technique to eliminate candidates.

    For each unsolved cell, try each candidate by placing it and solving with all other rules.
    If a contradiction is reached, that candidate can be eliminated.

    Args:
        grid (Grid): The Sudoku grid to apply the rule to.

    Returns:
        bool: True if any candidates were eliminated, False otherwise.
    """
    unsolved = sorted(
        (cell for cell in grid if cell.value is None),
        key=lambda c: len(c.candidates),
    )

    changed = False
    for cell in unsolved:
        candidates_to_remove: set[int] = set()
        for candidate in cell.candidates:
            trial_grid = grid.duplicate()
            trial_cell = trial_grid[cell.coord]
            if trial_cell is None:
                continue

            set_cell_value(trial_grid, trial_cell, candidate)

            solver = Solver(trial_grid, use_nishio=False)
            solver.solve()

            if not solver.is_valid():
                candidates_to_remove.add(candidate)

        if candidates_to_remove:
            cell.candidates -= candidates_to_remove
            changed = True

    return changed
