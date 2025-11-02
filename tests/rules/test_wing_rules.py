from model import Grid, Point
from rules.wing_rules import (
    apply_xy_wing_rule,
    apply_xyz_wing_rule,
)


# Note that in these tests the candidates are forced on the cells
# to ensure that the rules can be applied. In a real Sudoku puzzle,
# candidates would be determined by the puzzle's initial state.


def test_apply_xy_wing_rule_reduces_candidates_for_box_line():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Pivot
    grid[Point(4, 4)].candidates = {1, 2}

    # Line Wing
    grid[Point(1, 4)].candidates = {1, 3}

    # Box Wing
    grid[Point(3, 3)].candidates = {2, 3}

    applied = apply_xy_wing_rule(grid)
    assert applied is True

    # Candidate 3 should be removed from cells that see both wings.
    assert sum(True for cell in grid if 3 in cell.candidates) == 75
    assert 3 not in grid[Point(0, 3)].candidates
    assert 3 not in grid[Point(1, 3)].candidates
    assert 3 not in grid[Point(2, 3)].candidates
    assert 3 not in grid[Point(3, 4)].candidates
    assert 3 not in grid[Point(5, 4)].candidates


def test_apply_xy_wing_rule_reduces_candidates_for_row_column():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Pivot
    grid[Point(4, 4)].candidates = {1, 2}

    # Row Wing
    grid[Point(1, 4)].candidates = {1, 3}

    # Column Wing
    grid[Point(4, 1)].candidates = {2, 3}

    applied = apply_xy_wing_rule(grid)
    assert applied is True

    # Candidate 3 should be removed from the cell that sees both wings.
    assert sum(True for cell in grid if 3 in cell.candidates) == 79
    assert 3 not in grid[Point(1, 1)].candidates


def test_apply_xy_wing_rule_returns_false_when_unable_to_update_candidates():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    assert apply_xy_wing_rule(grid) is False


def test_apply_xy_wing_rule_returns_false_when_grid_is_complete():
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

    assert apply_xy_wing_rule(grid) is False


def test_apply_xyz_wing_rule_reduces_candidates():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Pivot
    grid[Point(4, 4)].candidates = {1, 2, 3}

    # Line Wing
    grid[Point(1, 4)].candidates = {1, 3}

    # Box Wing
    grid[Point(3, 3)].candidates = {2, 3}

    applied = apply_xyz_wing_rule(grid)
    assert applied is True

    # Candidate 3 should be removed from cells that see both wings.
    assert sum(True for cell in grid if 3 in cell.candidates) == 79
    assert 3 not in grid[Point(3, 4)].candidates
    assert 3 not in grid[Point(5, 4)].candidates


def test_apply_xyz_wing_rule_returns_false_when_unable_to_update_candidates():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    assert apply_xyz_wing_rule(grid) is False


def test_apply_xyz_wing_rule_returns_false_when_grid_is_complete():
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

    assert apply_xyz_wing_rule(grid) is False
