from model.grid import Grid
from model.point import Point


def _intersection_iter(grid: Grid):
    for cr in range(9):
        for b in range(3):
            intersection = grid.get_column_cells(cr, b)
            block = grid.get_block_cells(Point(cr // 3, b)).difference(intersection)
            column = grid.get_column_cells(cr).difference(intersection)
            yield intersection, block, column

            intersection = grid.get_row_cells(cr, b)
            block = grid.get_block_cells(Point(b, cr // 3)).difference(intersection)
            row = grid.get_row_cells(cr).difference(intersection)
            yield intersection, block, row


def apply_locked_candidates_rule(grid: Grid) -> bool:
    """
    Reduce candidates across all cells where the hidden triples rule applies.

    Args:
        grid (Grid): The Sudoku grid to apply the solver to.

    Returns:
        bool: True if the solver could be applied, False otherwise.
    """
    applied = False

    for (intersection, block, colrow) in _intersection_iter(grid):
        intersection_candidates = { candidate for cell in intersection for candidate in cell.candidates }
        block_candidates = { candidate for cell in block for candidate in cell.candidates }
        valid_candidates = intersection_candidates.difference(block_candidates)
        for cell in colrow:
            if cell.value is not None:
                continue

            applied |= len(cell.candidates.intersection(valid_candidates)) > 0
            cell.candidates = cell.candidates.difference(valid_candidates)

        colrow_candidates = { candidate for cell in colrow for candidate in cell.candidates }
        valid_candidates = intersection_candidates.difference(colrow_candidates)
        for cell in block:
            if cell.value is not None:
                continue

            applied |= len(cell.candidates.intersection(valid_candidates)) > 0
            cell.candidates = cell.candidates.difference(valid_candidates)

    return applied
