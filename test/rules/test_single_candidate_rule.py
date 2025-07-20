from model import Grid, Point
from rules import solve_single_candidates


def test_solve_single_candidates_inserts_values_for_single_candidates():
    grid = Grid.from_rows_notation(
        [
            "12.456789",  # Should be a 3
            "4.6789123",  # Should be a 5
            ".89123456",  # Should be a 7
            "23456.891",  # Should be a 7
            "5678.1234",  # Should be a 9
            "891.34567",  # Should be a 2
            "34567891.",  # Should be a 2
            "6789123.5",  # Should be a 4
            "912345.78",  # Should be a 6
        ]
    )

    solve_single_candidates(grid)

    assert grid[Point(2, 0)].value == 3
    assert grid[Point(1, 1)].value == 5
    assert grid[Point(0, 2)].value == 7
    assert grid[Point(5, 3)].value == 7
    assert grid[Point(4, 4)].value == 9
    assert grid[Point(3, 5)].value == 2
    assert grid[Point(8, 6)].value == 2
    assert grid[Point(7, 7)].value == 4
    assert grid[Point(6, 8)].value == 6


def test_solve_single_candidates_returns_true_when_able_to_solve_at_least_one_cell():
    grid = Grid.from_rows_notation(
        [
            "12.456789",
            "4.6789123",
            ".89123456",
            "23456.891",
            "5678.1234",
            "891.34567",
            "34567891.",
            "6789123.5",
            "912345.78",
        ]
    )

    assert solve_single_candidates(grid) is True


def test_solve_single_candidates_returns_false_when_no_single_candidates():
    grid = Grid.from_rows_notation(  # All 5s and 9s missing.
        [
            "1234.678.",
            "4.678.123",
            "78.1234.6",
            "234.678.1",
            ".678.1234",
            "8.1234.67",
            "34.678.12",
            "678.1234.",
            ".1234.678",
        ]
    )

    assert solve_single_candidates(grid) is False


def test_solve_single_candidates_returns_false_when_grid_complete():
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

    assert solve_single_candidates(grid) is False
