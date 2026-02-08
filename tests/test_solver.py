from unittest.mock import patch

import pytest
from model import Grid, Point
from solver import Solver


BASE_GRID = [
    ".7.2.8.31",
    "48.3.7...",
    "9.3..4758",
    ".4687...3",
    "89..3.56.",
    "..792.81.",
    "754.12...",
    "...7.3145",
    "3.8.4.2.6",
]


def test_init_stores_grid():
    grid = Grid([[1, 2, 3, 4, 5, 6, 7, 8, 9]] * 9)
    solver = Solver(grid)

    assert solver.grid is grid


def test_init_defaults_use_nishio_to_true():
    grid = Grid([[1, 2, 3, 4, 5, 6, 7, 8, 9]] * 9)
    solver = Solver(grid)

    assert solver.use_nishio is True


def test_init_stores_use_nishio():
    grid = Grid([[1, 2, 3, 4, 5, 6, 7, 8, 9]] * 9)
    solver = Solver(grid, use_nishio=False)

    assert solver.use_nishio is False


def test_solve_calls_apply_rules_until_it_returns_false():
    grid = Grid.from_rows_notation(BASE_GRID)
    solver = Solver(grid)

    with patch("solver.apply_rules", side_effect=[True, True, False]) as mock_apply:
        solver.solve()

    assert mock_apply.call_count == 3
    for call in mock_apply.call_args_list:
        assert call[0][0] is grid
        assert call[0][1] is True


def test_solve_passes_use_nishio_to_apply_rules():
    grid = Grid.from_rows_notation(BASE_GRID)
    solver = Solver(grid, use_nishio=False)

    with patch("solver.apply_rules", return_value=False) as mock_apply:
        solver.solve()

    mock_apply.assert_called_once_with(grid, False)


def test_is_solved_returns_true_when_all_cells_have_values():
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
    solver = Solver(grid)

    assert solver.is_solved() is True


def test_is_solved_returns_false_when_some_cells_are_empty():
    grid = Grid.from_rows_notation(
        [
            "123456789",
            "456789123",
            "789123456",
            "23456789.",
            "567891234",
            "891234567",
            "345678912",
            "678912345",
            "912345678",
        ]
    )
    solver = Solver(grid)

    assert solver.is_solved() is False


def test_is_valid_returns_true_when_solve_is_valid():
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
    solver = Solver(grid)

    assert solver.is_valid() is True


def test_is_valid_returns_true_when_initial_state_contains_no_conflicts():
    grid = Grid.from_rows_notation(
        [
            ".9825....",
            "..3.9....",
            "26..7.84.",
            ".3......8",
            "......2.6",
            ".7....53.",
            ".8.3..6..",
            "........4",
            "624..8...",
        ]
    )
    solver = Solver(grid)

    assert solver.is_valid() is True


def test_is_valid_returns_false_when_value_is_repeated_on_row():
    grid = Grid.from_rows_notation(
        [
            ".1.....1.",
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
    solver = Solver(grid)

    assert solver.is_valid() is False


def test_is_valid_returns_false_when_value_is_repeated_on_column():
    grid = Grid.from_rows_notation(
        [
            ".........",
            ".1.......",
            ".........",
            ".........",
            ".........",
            ".........",
            ".........",
            ".1.......",
            ".........",
        ]
    )
    solver = Solver(grid)

    assert solver.is_valid() is False


def test_is_valid_returns_false_when_value_is_repeated_in_block():
    grid = Grid.from_rows_notation(
        [
            ".........",
            ".........",
            ".........",
            "...1.....",
            ".........",
            ".....1...",
            ".........",
            ".........",
            ".........",
        ]
    )
    solver = Solver(grid)

    assert solver.is_valid() is False


def test_is_valid_returns_true_when_grid_is_entirely_empty():
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

    solver = Solver(grid)

    assert solver.is_valid() is True


def test_is_valid_returns_false_when_cell_has_no_candidates():
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

    # Manually clear candidates for one cell to simulate a contradiction
    grid[Point(0, 0)].candidates = set()

    solver = Solver(grid)

    assert solver.is_valid() is False
