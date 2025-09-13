from itertools import combinations
from model.grid import Grid
from model.point import Point

def apply_fish_rule(grid: Grid, size: int) -> bool:
    """
    Apply the fish rule (X-Wing, Swordfish, Jellyfish) to the Sudoku grid.

    Args:
        grid (Grid): The Sudoku grid to apply the solver to.
        size (int): The size of the fish pattern (2 for X-Wing, 3 for Swordfish, 4 for Jellyfish).

    Returns:
        bool: True if the solver could be applied, False otherwise.
    """
    if size < 2 or size > 4:
        raise ValueError("Size must be between 2 and 4.")

    applied = False

    # Check rows for fish patterns
    for candidate in range(1, 10):
        rows_with_candidate = [
            r for r in range(9) if sum(1 for c in range(9) if candidate in grid[Point(c, r)].candidates) > 0
        ]
        if len(rows_with_candidate) < size:
            continue

        for row_comb in combinations(rows_with_candidate, size):
            cols = {c for r in row_comb for c in range(9) if candidate in grid[Point(c, r)].candidates}

            if len(cols) == size:
                # Found a fish pattern
                for c in cols:
                    for r in range(9):
                        if r not in row_comb and candidate in grid[Point(c, r)].candidates:
                            grid[Point(c, r)].candidates -= { candidate, }
                            applied = True

    # Check columns for fish patterns
    for candidate in range(1, 10):
        cols_with_candidate = [
            c for c in range(9) if sum(1 for r in range(9) if candidate in grid[Point(c, r)].candidates) > 0
        ]
        if len(cols_with_candidate) < size:
            continue

        for col_comb in combinations(cols_with_candidate, size):
            rows = {r for c in col_comb for r in range(9) if candidate in grid[Point(c, r)].candidates}

            if len(rows) == size:
                # Found a fish pattern
                for r in rows:
                    for c in range(9):
                        if c not in col_comb and candidate in grid[Point(c, r)].candidates:
                            grid[Point(c, r)].candidates -= { candidate, }
                            applied = True

    return applied
