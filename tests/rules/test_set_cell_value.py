from model import Grid, Point
from rules.set_cell_value import set_cell_value


def test_set_cell_updates_the_cell_value():
    grid = Grid.from_rows_notation(
        [
            ".........",
            ".........",
            ".........",
            ".........",
            ".........",
            ".........",
            ".........",
            ".........",
            ".........",
        ]
    )
    cell = grid[Point(2, 2)]

    set_cell_value(grid, cell, 5)

    assert cell.value == 5


def test_set_cell_updates_neighbours_candidates():
    grid = Grid.from_rows_notation(
        [
            ".........",
            ".........",
            ".........",
            ".........",
            ".........",
            ".........",
            ".........",
            ".........",
            ".........",
        ]
    )
    cell = grid[Point(2, 2)]
    block_cell = grid[Point(1, 1)]
    row_cell = grid[Point(5, 2)]
    col_cell = grid[Point(2, 5)]
    unrelated_cell = grid[Point(5, 5)]

    # Sanity check: ensure these cells have 5 among their candidates initially
    assert 5 in block_cell.candidates
    assert 5 in row_cell.candidates
    assert 5 in col_cell.candidates
    assert 5 in unrelated_cell.candidates

    set_cell_value(grid, cell, 5)

    # Validate that neighbour cells have lost 5 as a candidate.
    assert 5 not in block_cell.candidates
    assert 5 not in row_cell.candidates
    assert 5 not in col_cell.candidates

    # Unrelated cell should still have 5 as a candidate.
    assert 5 in unrelated_cell.candidates
