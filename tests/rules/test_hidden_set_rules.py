from model import Grid, Point
from rules.hidden_set_rules import (
    apply_hidden_single_rule,
    apply_hidden_pairs_rule,
    apply_hidden_triples_rule,
)


# Note that in these tests the candidates are forced on the cells
# to ensure that the rules can be applied. In a real Sudoku puzzle,
# candidates would be determined by the puzzle's initial state.


def test_apply_hidden_single_rule_reduces_candidates_in_block():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a hidden single in the first block.
    # Cell (1, 1) is the only cell with candidate 4.
    for x in range(3):
        for y in range(3):
            if x == 1 and y == 1:
                continue

            grid[Point(x, y)].candidates -= {4}

    apply_hidden_single_rule(grid)

    # Cell (1, 1) now only has candidate 4.
    assert grid[Point(1, 1)].candidates == {4}

    # Other cells in the block still have their candidates intact.
    for x in range(3):
        for y in range(3):
            if x == 1 and y == 1:
                continue

            assert grid[Point(x, y)].candidates == {1, 2, 3, 5, 6, 7, 8, 9}


def test_apply_hidden_single_rule_reduces_candidates_in_column():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a hidden single in the third column.
    # Cell (2, 7) is the only cell with candidate 4.
    for y in range(9):
        if y == 7:
            continue

        grid[Point(2, y)].candidates -= {4}

    apply_hidden_single_rule(grid)

    # Cell (2, 7) now only has candidate 4.
    assert grid[Point(2, 7)].candidates == {4}

    # Other cells in the block still have their candidates intact.
    for y in range(9):
        if y == 7:
            continue

        assert grid[Point(2, y)].candidates == {1, 2, 3, 5, 6, 7, 8, 9}


def test_apply_hidden_single_rule_reduces_candidates_in_row():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a hidden single in the third row.
    # Cell (7, 2) is the only cell with candidate 4.
    for x in range(9):
        if x == 7:
            continue

        grid[Point(x, 2)].candidates -= {4}

    apply_hidden_single_rule(grid)

    # Cell (7, 2) now only has candidate 4.
    assert grid[Point(7, 2)].candidates == {4}

    # Other cells in the block still have their candidates intact.
    for x in range(9):
        if x == 7:
            continue

        assert grid[Point(x, 2)].candidates == {1, 2, 3, 5, 6, 7, 8, 9}


def test_apply_hidden_single_rule_returns_true_when_able_to_update_candidates():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a hidden single in the third row.
    # Cell (7, 2) is the only cell with candidate 4.
    for x in range(9):
        if x == 7:
            continue

        grid[Point(x, 2)].candidates -= {4}

    assert apply_hidden_single_rule(grid) is True


def test_apply_hidden_single_rule_returns_false_when_unable_to_update_candidates():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    assert apply_hidden_single_rule(grid) is False


def test_apply_hidden_single_rule_returns_false_when_grid_is_complete():
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

    assert apply_hidden_single_rule(grid) is False


def test_apply_hidden_pairs_rule_reduces_candidates_in_block():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a hidden pair in the first block.
    # Cells (1, 1) and (2, 2) are the only cells with candidates 2 and 5.
    for x in range(3):
        for y in range(3):
            if (x == 1 and y == 1) or (x == 2 and y == 2):
                continue

            grid[Point(x, y)].candidates -= {2, 5}

    apply_hidden_pairs_rule(grid)

    # Cells with pairs now only have candidates 2 and 5.
    assert grid[Point(1, 1)].candidates == {2, 5}
    assert grid[Point(2, 2)].candidates == {2, 5}

    # Other cells in the block still have their candidates intact.
    for x in range(3):
        for y in range(3):
            if (x == 1 and y == 1) or (x == 2 and y == 2):
                continue

            assert grid[Point(x, y)].candidates == {1, 3, 4, 6, 7, 8, 9}


def test_apply_hidden_pairs_rule_reduces_candidates_in_column():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a hidden single in the third column.
    # Cells (2, 4) and (2, 8) are the only cells with candidates 2 and 5.
    for y in range(9):
        if y == 4 or y == 8:
            continue

        grid[Point(2, y)].candidates -= {2, 5}

    apply_hidden_pairs_rule(grid)

    # Cells with pairs now only have candidates 2 and 5.
    assert grid[Point(2, 4)].candidates == {2, 5}
    assert grid[Point(2, 8)].candidates == {2, 5}

    # Other cells in the block still have their candidates intact.
    for y in range(9):
        if y == 4 or y == 8:
            continue

        assert grid[Point(2, y)].candidates == {1, 3, 4, 6, 7, 8, 9}


def test_apply_hidden_pairs_rule_reduces_candidates_in_row():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a hidden single in the third row.
    # Cells (2, 4) and (2, 8) are the only cells with candidates 2 and 5.
    for x in range(9):
        if x == 4 or x == 8:
            continue

        grid[Point(x, 2)].candidates -= {2, 5}

    apply_hidden_pairs_rule(grid)

    # Cells with pairs now only have candidates 2 and 5.
    assert grid[Point(4, 2)].candidates == {2, 5}
    assert grid[Point(8, 2)].candidates == {2, 5}

    # Other cells in the block still have their candidates intact.
    for x in range(9):
        if x == 4 or x == 8:
            continue

        assert grid[Point(x, 2)].candidates == {1, 3, 4, 6, 7, 8, 9}


def test_apply_hidden_pairs_rule_returns_true_when_able_to_update_candidates():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a hidden single in the third row.
    # Cells (2, 4) and (2, 8) are the only cells with candidates 2 and 5.
    for x in range(9):
        if x == 4 or x == 8:
            continue

        grid[Point(x, 2)].candidates -= {2, 5}

    assert apply_hidden_pairs_rule(grid) is True


def test_apply_hidden_pairs_rule_handles_one_candidate_missing_from_cell():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a hidden pair in the third column.
    # Cells (2, 4) and (2, 8) are the only cells with candidate 2.
    # Cell (2, 8) is the only cell with candidate 5.
    for y in (0, 1, 2, 3, 5, 6, 7):
        grid[Point(2, y)].candidates -= {2, 5}

    grid[Point(2, 4)].candidates -= {5}

    apply_hidden_pairs_rule(grid)

    # Affected cells now only contain their hidden pair.
    assert grid[Point(2, 4)].candidates == {2}
    assert grid[Point(2, 8)].candidates == {2, 5}

    # Other cells in the block still have their candidates intact.
    for y in range(9):
        if y == 4 or y == 8:
            continue

        assert grid[Point(2, y)].candidates == {1, 3, 4, 6, 7, 8, 9}


def test_apply_hidden_pairs_rule_returns_false_when_unable_to_update_candidates():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    assert apply_hidden_pairs_rule(grid) is False


def test_apply_hidden_pairs_rule_returns_false_when_grid_is_complete():
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

    assert apply_hidden_pairs_rule(grid) is False


def test_apply_hidden_triples_rule_reduces_candidates_in_block():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a hidden triple in the first block.
    # Cells (0, 0), (1, 1) and (2, 2) are the only cells with candidates 2, 4 and 7.
    for x in range(3):
        for y in range(3):
            if x == y:
                continue

            grid[Point(x, y)].candidates -= {2, 4, 7}

    apply_hidden_triples_rule(grid)

    # Affected cells now only have candidate 2, 4 and 7.
    assert grid[Point(0, 0)].candidates == {2, 4, 7}
    assert grid[Point(1, 1)].candidates == {2, 4, 7}
    assert grid[Point(2, 2)].candidates == {2, 4, 7}

    # Other cells in the block still have their candidates intact.
    for x in range(3):
        for y in range(3):
            if x == y:
                continue

            assert grid[Point(x, y)].candidates == {1, 3, 5, 6, 8, 9}


def test_apply_hidden_triples_rule_reduces_candidates_in_column():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a hidden triple in the third column.
    # Cells (2, 0), (2, 3) and (2, 6) are the only cells with candidates 2, 4 and 7.
    for y in range(9):
        if y % 3 == 0:
            continue

        grid[Point(2, y)].candidates -= {2, 4, 7}

    apply_hidden_triples_rule(grid)

    # Affected cells now only have candidate 2, 4 and 7.
    assert grid[Point(2, 0)].candidates == {2, 4, 7}
    assert grid[Point(2, 3)].candidates == {2, 4, 7}
    assert grid[Point(2, 6)].candidates == {2, 4, 7}

    # Other cells in the block still have their candidates intact.
    for y in range(9):
        if y % 3 == 0:
            continue

        assert grid[Point(2, y)].candidates == {1, 3, 5, 6, 8, 9}


def test_apply_hidden_triples_rule_reduces_candidates_in_row():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a hidden single in the third row.
    # Cells (0, 2), (3, 2) and (6, 2) are the only cells with candidates 2, 4 and 7.
    for x in range(9):
        if x % 3 == 0:
            continue

        grid[Point(x, 2)].candidates -= {2, 4, 7}

    apply_hidden_triples_rule(grid)

    # Affected cells now only have candidate 2, 4 and 7.
    assert grid[Point(0, 2)].candidates == {2, 4, 7}
    assert grid[Point(3, 2)].candidates == {2, 4, 7}
    assert grid[Point(6, 2)].candidates == {2, 4, 7}

    # Other cells in the block still have their candidates intact.
    for x in range(9):
        if x % 3 == 0:
            continue

        assert grid[Point(x, 2)].candidates == {1, 3, 5, 6, 8, 9}


def test_apply_hidden_triples_rule_returns_true_when_able_to_update_candidates():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a hidden single in the third row.
    # Cells (0, 2), (3, 2) and (6, 2) are the only cells with candidates 2, 4 and 7.
    for x in range(9):
        if x % 3 == 0:
            continue

        grid[Point(x, 2)].candidates -= {2, 4, 7}

    assert apply_hidden_triples_rule(grid) is True


def test_apply_hidden_triples_rule_handles_candidates_missing_from_cells():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    # Set candidates for a hidden triple in the third column.
    # Cell (2, 0) has candidates 2 and 4.
    # Cell (2, 3) has candidates 2 and 7.
    # Cell (2, 6) has candidates 4 and 7.
    # Between them, they cover all candidates 2, 4 and 7.
    # Other cells do not have candidates 2, 4 or 7.
    for y in range(9):
        if y % 3 == 0:
            continue

        grid[Point(2, y)].candidates -= {2, 4, 7}

    grid[Point(2, 0)].candidates -= {7}
    grid[Point(2, 3)].candidates -= {4}
    grid[Point(2, 6)].candidates -= {2}

    apply_hidden_triples_rule(grid)

    # Affected cells now only contain their hidden triple candidates.
    assert grid[Point(2, 0)].candidates == {2, 4}
    assert grid[Point(2, 3)].candidates == {2, 7}
    assert grid[Point(2, 6)].candidates == {4, 7}

    # Other cells in the block still have their candidates intact.
    for y in range(9):
        if y % 3 == 0:
            continue

        assert grid[Point(2, y)].candidates == {1, 3, 5, 6, 8, 9}


def test_apply_hidden_triples_rule_returns_false_when_unable_to_update_candidates():
    grid = Grid.from_rows_notation(["." * 9] * 9)

    assert apply_hidden_triples_rule(grid) is False


def test_apply_hidden_triples_rule_returns_false_when_grid_is_complete():
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

    assert apply_hidden_triples_rule(grid) is False
