from model import Grid, Point
from rules.locked_candidates_rule import apply_locked_candidates_rule


# Note that in these tests the candidates are forced on the cells
# to ensure that the rules can be applied. In a real Sudoku puzzle,
# candidates would be determined by the puzzle's initial state.


def test_apply_locked_candidates_rule_for_row_intersection_removes_row_candidates():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a locked candidate in the last three cells of row 5.
    # The top and bottom row of the middle-right block do not have candidate 6.
    for x in range(6, 9):
        grid[Point(x, 3)].candidates -= {6}
        grid[Point(x, 5)].candidates -= {6}

    apply_locked_candidates_rule(grid)

    # The first 6 cells in row 5 should now not have candidate 6.
    for x in range(6):
        assert 6 not in grid[Point(x, 4)].candidates


def test_apply_locked_candidates_rule_for_row_intersection_removes_block_candidates():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a locked candidate in the last three cells of row 5.
    # The first 6 cells of row 5 do not have candidate 6.
    for x in range(6):
        grid[Point(x, 4)].candidates -= {6}

    apply_locked_candidates_rule(grid)

    # The top and bottom row of the middle-right block should now not have candidate 6.
    for x in range(6, 9):
        assert 6 not in grid[Point(x, 3)].candidates
        assert 6 not in grid[Point(x, 5)].candidates


def test_apply_locked_candidates_rule_for_column_intersection_removes_column_candidates():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a locked candidate in the last three cells of column 5.
    # The left and right column of the centre-bottom block do not have candidate 6.
    for y in range(6, 9):
        grid[Point(3, y)].candidates -= {6}
        grid[Point(5, y)].candidates -= {6}

    apply_locked_candidates_rule(grid)

    # The first 6 cells in column 5 should now not have candidate 6.
    for y in range(6):
        assert 6 not in grid[Point(4, y)].candidates


def test_apply_locked_candidates_rule_for_column_intersection_removes_block_candidates():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a locked candidate in the last three cells of column 5.
    # The first 6 cells of column 5 do not have candidate 6.
    for y in range(6):
        grid[Point(4, y)].candidates -= {6}

    apply_locked_candidates_rule(grid)

    # The left and right column of the centre-bottom block should now not have candidate 6.
    for y in range(6, 9):
        assert 6 not in grid[Point(3, y)].candidates
        assert 6 not in grid[Point(5, y)].candidates


def test_apply_locked_candidates_rule_returns_true_when_able_to_update_candidates():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set up locked candidates in column 5.
    for y in range(6):
        grid[Point(4, y)].candidates -= {6}

    assert apply_locked_candidates_rule(grid) is True


def test_apply_locked_candidates_rule_returns_false_when_unable_to_update_candidates():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    assert apply_locked_candidates_rule(grid) is False


def test_apply_locked_candidates_rule_returns_false_when_grid_is_complete():
    grid = Grid.from_rows_notation(
        [
            "123456789",
            "456789123",
            "789123456",
            "234567891",
            "567891234",
            "891234567",
            "345678912",
            "678912345",
            "912345678",
        ]
    )

    assert apply_locked_candidates_rule(grid) is False
