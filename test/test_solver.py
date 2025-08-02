from unittest.mock import call, patch

import pytest
from model import Grid
from solver import Solver


@pytest.fixture
def mock_single_candidates():
    with patch("solver.apply_single_candidate_rule") as mock:
        yield mock


@pytest.fixture
def mock_naked_pairs():
    with patch("solver.apply_naked_pairs_rule") as mock:
        yield mock


@pytest.fixture
def mock_naked_triples():
    with patch("solver.apply_naked_triples_rule") as mock:
        yield mock


def test_init_stores_grid():
    grid = Grid([[1, 2, 3, 4, 5, 6, 7, 8, 9]] * 9)
    solver = Solver(grid)

    assert solver.grid is grid


def test_solve_applies_single_candidates(
    mock_single_candidates, mock_naked_pairs, mock_naked_triples
):
    mock_single_candidates.side_effect = [True, True, False]
    mock_naked_pairs.return_value = False
    mock_naked_triples.return_value = False

    grid = Grid.from_rows_notation(
        [
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
    )
    solver = Solver(grid)

    solver.solve()

    mock_single_candidates.assert_has_calls([call(grid), call(grid), call(grid)])
    assert mock_single_candidates.call_count == 3


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
