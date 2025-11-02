from itertools import chain, repeat
from unittest.mock import call, patch, DEFAULT

import pytest
from model import Grid
from solver import Solver


@pytest.fixture
def all_mocks():
    with patch.multiple(
        "solver",
        apply_single_candidate_rule=DEFAULT,
        apply_naked_pairs_rule=DEFAULT,
        apply_naked_triples_rule=DEFAULT,
        apply_hidden_single_rule=DEFAULT,
        apply_hidden_pairs_rule=DEFAULT,
        apply_hidden_triples_rule=DEFAULT,
        apply_locked_candidates_rule=DEFAULT,
        apply_fish_rule=DEFAULT,
        apply_xy_wing_rule=DEFAULT,
        apply_xyz_wing_rule=DEFAULT,
    ) as mocks:
        yield mocks


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


@pytest.mark.parametrize(
    "rule_attr",
    [
        "apply_single_candidate_rule",
        "apply_naked_pairs_rule",
        "apply_naked_triples_rule",
        "apply_hidden_single_rule",
        "apply_hidden_pairs_rule",
        "apply_hidden_triples_rule",
        "apply_locked_candidates_rule",
        "apply_xy_wing_rule",
        "apply_xyz_wing_rule",
    ],
)
def test_each_rule_applies_when_earlier_rules_return_false(all_mocks, rule_attr):
    # Make every rule return False by default
    for mock in all_mocks.values():
        mock.return_value = False

    # The rule under test should be the only one that returns True twice then False
    all_mocks[rule_attr].side_effect = [True, True, False]

    grid = Grid.from_rows_notation(BASE_GRID)
    solver = Solver(grid)

    # Act
    solver.solve()

    # Assert: the rule under test was invoked three times with the grid
    all_mocks[rule_attr].assert_has_calls([call(grid), call(grid), call(grid)])
    assert all_mocks[rule_attr].call_count == 3


def test_fish_rule_call_patterns(all_mocks):
    # Ensure non-fish rules do nothing
    for name, mock in all_mocks.items():
        if name != "apply_fish_rule":
            mock.return_value = False

    fish = all_mocks["apply_fish_rule"]
    fish.side_effect = [True, True, False, False, False]

    grid = Grid.from_rows_notation(BASE_GRID)
    solver = Solver(grid)

    solver.solve()

    # Expect three calls with size=2, then one with size=3 and one with size=4 (in sequence)
    expected_calls = [
        call(grid, size=2),
        call(grid, size=2),
        call(grid, size=2),
        call(grid, size=3),
        call(grid, size=4),
    ]
    fish.assert_has_calls(expected_calls)
    assert fish.call_count == 5


def test_only_applies_latter_rules_when_earlier_rules_fail(all_mocks):
    for mock in all_mocks.values():
        mock.side_effect = chain([True], repeat(False))

    grid = Grid.from_rows_notation(BASE_GRID)
    solver = Solver(grid)

    solver.solve()

    assert all_mocks["apply_single_candidate_rule"].call_count == 11
    assert all_mocks["apply_naked_pairs_rule"].call_count == 10
    assert all_mocks["apply_naked_triples_rule"].call_count == 9
    assert all_mocks["apply_hidden_single_rule"].call_count == 8
    assert all_mocks["apply_hidden_pairs_rule"].call_count == 7
    assert all_mocks["apply_hidden_triples_rule"].call_count == 6
    assert all_mocks["apply_locked_candidates_rule"].call_count == 5
    # apply_fish_rule is called 4 + 3n where n is number of rules below it.
    assert all_mocks["apply_fish_rule"].call_count == 10
    assert all_mocks["apply_xy_wing_rule"].call_count == 3
    assert all_mocks["apply_xyz_wing_rule"].call_count == 2


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
