from model.grid import Grid
from itertools import combinations


def _apply_naked_set_rule(grid: Grid, size: int) -> bool:
    """
    Reduce candidates across all cells where a naked set can be found.

    Args:
        grid (Grid): The Sudoku grid to apply the solver to.
        size (int): The size of the naked set (2 for pairs, 3 for triples, etc).

    Returns:
        bool: True if the solver could be applied, False otherwise.
    """
    applied = False

    for region in grid.region_iter():
        # Find all naked sets in the region
        incomplete_cells = [cell for cell in region if cell.value is None]
        naked_sets = [
            cells
            for cells in combinations(incomplete_cells, size)
            if len(set().union(*(cell.candidates for cell in cells))) == size
        ]

        # Remove candidates from other cells in the region
        for naked_set in naked_sets:
            candidates_to_remove = set().union(*(cell.candidates for cell in naked_set))
            for cell in region:
                if (
                    cell in naked_set
                    or cell.value is not None
                    or cell.candidates.isdisjoint(candidates_to_remove)
                ):
                    continue

                cell.candidates -= candidates_to_remove
                applied = True

    return applied


def apply_naked_pairs_rule(grid: Grid) -> bool:
    """
    Reduce candidates across all cells where the naked pairs rule applies.

    Args:
        grid (Grid): The Sudoku grid to apply the solver to.

    Returns:
        bool: True if the solver could be applied, False otherwise.
    """
    return _apply_naked_set_rule(grid, size=2)


def apply_naked_triples_rule(grid: Grid) -> bool:
    """
    Reduce candidates across all cells where the naked triples rule applies.

    Args:
        grid (Grid): The Sudoku grid to apply the solver to.

    Returns:
        bool: True if the solver could be applied, False otherwise.
    """
    return _apply_naked_set_rule(grid, size=3)
