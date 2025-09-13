from model import Grid
from rules.set_cell_value import set_cell_value


def apply_single_candidate_rule(grid: Grid) -> bool:
    """
    Solve all possible cells using the single candidate rule.

    Args:
        grid (Grid): The Sudoku grid to apply the solver to.

    Returns:
        bool: True if the solver could be applied, False otherwise.
    """
    applied = False

    for cell in grid:
        if cell.value is not None:
            continue

        if len(cell.candidates) == 1:
            set_cell_value(grid, cell, cell.candidates.pop())
            applied = True

    return applied
