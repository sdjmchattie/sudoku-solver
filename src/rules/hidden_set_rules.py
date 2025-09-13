from collections import Counter
from model import Grid
from itertools import combinations


ALL_CANDIDATES = set(range(1, 10))


def _apply_hidden_set_rule(grid: Grid, size: int) -> bool:
    """
    Reduce candidates across all cells where a hidden set can be found.

    Args:
        grid (Grid): The Sudoku grid to apply the solver to.
        size (int): The size of the hidden set (2 for pairs, 3 for triples, etc).

    Returns:
        bool: True if the solver could be applied, False otherwise.
    """
    applied = False

    for region in grid.region_iter():
        # Create list of candidates in the region
        counts = Counter(candidate for cell in region for candidate in cell.candidates)

        valid_candidates = {
            candidate for candidate, count in counts.items() if count <= size
        }

        # Work through all possible combinations of valid candidates
        for combination in combinations(valid_candidates, size):
            # Convert the tuple to a set
            set_candidates = set(combination)

            # Get a list of all the cells with any candidate
            affected_cells = [
                cell for cell in region if set_candidates.intersection(cell.candidates)
            ]

            # Move on if the number of affected cells doesn't match the set size
            if len(affected_cells) != size:
                continue

            # Found a valid hidden set!
            complementary_candidates = ALL_CANDIDATES - set_candidates
            for cell in affected_cells:
                if len(cell.candidates) > size:
                    applied = True

                cell.candidates -= complementary_candidates

    return applied


def apply_hidden_single_rule(grid: Grid) -> bool:
    """
    Reduce candidates across all cells where the hidden pairs rule applies.

    Args:
        grid (Grid): The Sudoku grid to apply the solver to.

    Returns:
        bool: True if the solver could be applied, False otherwise.
    """
    return _apply_hidden_set_rule(grid, size=1)


def apply_hidden_pairs_rule(grid: Grid) -> bool:
    """
    Reduce candidates across all cells where the hidden pairs rule applies.

    Args:
        grid (Grid): The Sudoku grid to apply the solver to.

    Returns:
        bool: True if the solver could be applied, False otherwise.
    """
    return _apply_hidden_set_rule(grid, size=2)


def apply_hidden_triples_rule(grid: Grid) -> bool:
    """
    Reduce candidates across all cells where the hidden triples rule applies.

    Args:
        grid (Grid): The Sudoku grid to apply the solver to.

    Returns:
        bool: True if the solver could be applied, False otherwise.
    """
    return _apply_hidden_set_rule(grid, size=3)
