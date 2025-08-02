from model import Grid, Point
from rules.naked_set_rules import apply_naked_pairs_rule, apply_naked_triples_rule


def test_apply_naked_pairs_rule_reduces_candidates_in_block():
    grid = Grid.from_rows_notation(
        [
            ".....6.89",  # Third cell could be 3 or 7
            ".........",
            "...12.456",  # First cell could be 3 or 7
            "..4567891",
            "...891234",
            "8.1234567",
            "..5678912",
            "...912345",
            "9.2345678",
        ]
    )

    # Sanity check: naked pair exists
    assert grid[Point(2, 0)].candidates == {3, 7}
    assert grid[Point(0, 2)].candidates == {3, 7}

    # Sanity check: other cells in the block contain the naked pair plus others
    for x in range(3):
        for y in range(3):
            if (x == 2 and y == 0) or (x == 0 and y == 2):
                continue

            assert 3 in grid[Point(x, y)].candidates
            assert 7 in grid[Point(x, y)].candidates
            assert len(grid[Point(x, y)].candidates) > 2

    apply_naked_pairs_rule(grid)

    # Naked pair still exists
    assert grid[Point(2, 0)].candidates == {3, 7}
    assert grid[Point(0, 2)].candidates == {3, 7}

    # Other cells in the block have had 3 and 7 candidates removed
    for x in range(3):
        for y in range(3):
            if (x == 2 and y == 0) or (x == 0 and y == 2):
                continue

            assert 3 not in grid[Point(x, y)].candidates
            assert 7 not in grid[Point(x, y)].candidates


def test_apply_naked_pairs_rule_reduces_candidates_in_column():
    grid = Grid.from_rows_notation(
        [
            ".234.67.9",
            "4567.9.23",  # Fifth cell could be 1 or 8
            "7.9..3456",
            "2345.7.9.",
            "567...234",
            ".9.2.4567",
            "3456..9.2",
            "67.9.2345",  # Fifth cell could be 1 or 8
            "9.23.567.",
        ]
    )

    # Sanity check: naked pair exists
    assert grid[Point(4, 1)].candidates == {1, 8}
    assert grid[Point(4, 7)].candidates == {1, 8}

    # Sanity check: other cells in the column contain the naked pair plus others
    for y in range(9):
        if y == 1 or y == 7:
            continue

        assert 1 in grid[Point(4, y)].candidates
        assert 8 in grid[Point(4, y)].candidates
        assert len(grid[Point(4, y)].candidates) > 2

    apply_naked_pairs_rule(grid)

    # Naked pair still exists
    assert grid[Point(4, 1)].candidates == {1, 8}
    assert grid[Point(4, 7)].candidates == {1, 8}

    # Other cells in the row have had 1 and 8 candidates removed
    for y in range(9):
        if y == 1 or y == 7:
            continue

        assert 1 not in grid[Point(4, y)].candidates
        assert 8 not in grid[Point(4, y)].candidates


def test_apply_naked_pairs_rule_reduces_candidates_in_row():
    grid = Grid.from_rows_notation(
        [
            ".23456.89",
            "456.89.23",
            ".89.23456",
            "23456.89.",
            ".........",  # Third and sixth cells could be 1 or 7
            "89.23456.",
            "3456.89.2",
            "6.89.2345",
            "9.23456.8",
        ]
    )

    # Sanity check: naked pair exists
    assert grid[Point(2, 4)].candidates == {1, 7}
    assert grid[Point(5, 4)].candidates == {1, 7}

    # Sanity check: other cells in the row contain the naked pair plus others
    for x in range(9):
        if x == 2 or x == 5:
            continue

        assert 1 in grid[Point(x, 4)].candidates
        assert 7 in grid[Point(x, 4)].candidates
        assert len(grid[Point(x, 4)].candidates) > 2

    apply_naked_pairs_rule(grid)

    # Naked pair still exists
    assert grid[Point(2, 4)].candidates == {1, 7}
    assert grid[Point(5, 4)].candidates == {1, 7}

    # Other cells in the row have had 1 and 7 candidates removed
    for x in range(9):
        if x == 2 or x == 5:
            continue

        assert 1 not in grid[Point(x, 4)].candidates
        assert 7 not in grid[Point(x, 4)].candidates


def test_apply_naked_pairs_rule_returns_true_when_able_to_update_candidates():
    grid = Grid.from_rows_notation(
        [
            ".23456.89",
            "456.89.23",
            ".89.23456",
            "23456.89.",
            ".........",
            "89.23456.",
            "3456.89.2",
            "6.89.2345",
            "9.23456.8",
        ]
    )

    assert apply_naked_pairs_rule(grid) is True


def test_apply_naked_pairs_rule_returns_false_when_unable_to_update_candidates():
    grid = Grid.from_rows_notation(
        ["........."] * 9  # Empty grid, no naked pairs
    )

    assert apply_naked_pairs_rule(grid) is False


def test_apply_naked_pairs_rule_returns_false_when_grid_is_complete():
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

    assert apply_naked_pairs_rule(grid) is False


def test_apply_naked_triples_rule_reduces_candidates_in_block():
    grid = Grid.from_rows_notation(
        [
            ".....6.89",  # Third cell could be 3, 5, or 7
            "....8912.",  # Second cell could be 3, 5, or 7
            "...12.4.6",  # First cell could be 3, 5, or 7
            "2.4.6.891",
            ".6.8912.4",
            "8912.4.6.",
            ".4.6.8912",
            "6.8912.4.",
            "912.4.6.8",
        ]
    )

    # Sanity check: naked pair exists
    assert grid[Point(2, 0)].candidates == {3, 5, 7}
    assert grid[Point(1, 1)].candidates == {3, 5, 7}
    assert grid[Point(0, 2)].candidates == {3, 5, 7}

    # Sanity check: other cells in the block contain the naked pair plus others
    for x in range(3):
        for y in range(3):
            if x + y == 2:
                continue

            assert 3 in grid[Point(x, y)].candidates
            assert 5 in grid[Point(x, y)].candidates
            assert 7 in grid[Point(x, y)].candidates
            assert len(grid[Point(x, y)].candidates) > 3

    apply_naked_triples_rule(grid)

    # Naked pair still exists
    assert grid[Point(2, 0)].candidates == {3, 5, 7}
    assert grid[Point(1, 1)].candidates == {3, 5, 7}
    assert grid[Point(0, 2)].candidates == {3, 5, 7}

    # Other cells in the block have had 3 and 7 candidates removed
    for x in range(3):
        for y in range(3):
            if x + y == 2:
                continue

            assert 3 not in grid[Point(x, y)].candidates
            assert 5 not in grid[Point(x, y)].candidates
            assert 7 not in grid[Point(x, y)].candidates


def test_apply_naked_triples_rule_reduces_candidates_in_column():
    grid = Grid.from_rows_notation(
        [
            ".234.67..",
            "4567...23",  # Fifth cell could be 1, 8, or 9
            "7....3456",
            "2345.7...",
            "567...234",  # fifth cell could be 1, 8, or 9
            "...2.4567",
            "3456....2",
            "67...2345",  # Fifth cell could be 1, 8, or 9
            "..23.567.",
        ]
    )

    # Sanity check: naked pair exists
    assert grid[Point(4, 1)].candidates == {1, 8, 9}
    assert grid[Point(4, 4)].candidates == {1, 8, 9}
    assert grid[Point(4, 7)].candidates == {1, 8, 9}

    # Sanity check: other cells in the column contain the naked pair plus others
    for y in range(9):
        if y % 3 == 1:
            continue

        assert 1 in grid[Point(4, y)].candidates
        assert 8 in grid[Point(4, y)].candidates
        assert 9 in grid[Point(4, y)].candidates
        assert len(grid[Point(4, y)].candidates) > 3

    apply_naked_triples_rule(grid)

    # Naked pair still exists
    assert grid[Point(4, 1)].candidates == {1, 8, 9}
    assert grid[Point(4, 4)].candidates == {1, 8, 9}
    assert grid[Point(4, 7)].candidates == {1, 8, 9}

    # Other cells in the row have had 1 and 8 candidates removed
    for y in range(9):
        if y % 3 == 1:
            continue

        assert 1 not in grid[Point(4, y)].candidates
        assert 8 not in grid[Point(4, y)].candidates
        assert 9 not in grid[Point(4, y)].candidates


def test_apply_naked_triples_rule_reduces_candidates_in_row():
    grid = Grid.from_rows_notation(
        [
            ".23.56.89",
            ".56.89.23",
            ".89.23.56",
            "23.56.89.",
            ".........",  # Cells 3, 6, and 9 could be 1, 4, or 7
            "89.23.56.",
            "3.56.89.2",
            "6.89.23.5",
            "9.23.56.8",
        ]
    )

    # Sanity check: naked pair exists
    assert grid[Point(2, 4)].candidates == {1, 4, 7}
    assert grid[Point(5, 4)].candidates == {1, 4, 7}
    assert grid[Point(8, 4)].candidates == {1, 4, 7}

    # Sanity check: other cells in the row contain the naked pair plus others
    for x in range(9):
        if x % 3 == 2:
            continue

        assert 1 in grid[Point(x, 4)].candidates
        assert 4 in grid[Point(x, 4)].candidates
        assert 7 in grid[Point(x, 4)].candidates
        assert len(grid[Point(x, 4)].candidates) > 2

    apply_naked_triples_rule(grid)

    # Naked pair still exists
    assert grid[Point(2, 4)].candidates == {1, 4, 7}
    assert grid[Point(5, 4)].candidates == {1, 4, 7}
    assert grid[Point(8, 4)].candidates == {1, 4, 7}

    # Other cells in the row have had 1 and 7 candidates removed
    for x in range(9):
        if x % 3 == 2:
            continue

        assert 1 not in grid[Point(x, 4)].candidates
        assert 4 not in grid[Point(x, 4)].candidates
        assert 7 not in grid[Point(x, 4)].candidates


def test_apply_naked_triples_rule_returns_true_when_able_to_update_candidates():
    grid = Grid.from_rows_notation(
        [
            ".23.56.89",
            ".56.89.23",
            ".89.23.56",
            "23.56.89.",
            ".........",
            "89.23.56.",
            "3.56.89.2",
            "6.89.23.5",
            "9.23.56.8",
        ]
    )

    assert apply_naked_triples_rule(grid) is True


def test_apply_naked_triples_rule_returns_false_when_unable_to_update_candidates():
    grid = Grid.from_rows_notation(
        ["........."] * 9  # Empty grid, no naked pairs
    )

    assert apply_naked_triples_rule(grid) is False


def test_apply_naked_triples_rule_returns_false_when_grid_is_complete():
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

    assert apply_naked_triples_rule(grid) is False
