from unittest.mock import patch, DEFAULT

import pytest
from model import Grid
from rules.all_rules import apply


@pytest.fixture
def grid():
    return Grid.from_rows_notation(
        [
            "..3456789",
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


@pytest.fixture
def all_mocks():
    with patch.multiple(
        "rules.all_rules",
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
        for mock in mocks.values():
            mock.return_value = False
        yield mocks


def test_apply_returns_true_when_a_rule_succeeds(all_mocks, grid):
    all_mocks["apply_hidden_single_rule"].return_value = True

    assert apply(grid, include_nishio=False) is True


def test_apply_returns_false_when_no_rules_succeed(all_mocks, grid):
    assert apply(grid, include_nishio=False) is False


def test_apply_tries_nishio_as_fallback(all_mocks, grid):
    with patch("rules.nishio_rule.apply_nishio_rule", return_value=True) as mock_nishio:
        result = apply(grid, include_nishio=True)

    assert result is True
    mock_nishio.assert_called_once_with(grid)


def test_apply_skips_nishio_when_disabled(all_mocks, grid):
    with patch("rules.nishio_rule.apply_nishio_rule") as mock_nishio:
        apply(grid, include_nishio=False)

    mock_nishio.assert_not_called()


def test_apply_short_circuits_on_first_success(all_mocks, grid):
    all_mocks["apply_single_candidate_rule"].return_value = True

    apply(grid, include_nishio=False)

    # Rules after single_candidate should not be called
    all_mocks["apply_naked_pairs_rule"].assert_not_called()
    all_mocks["apply_hidden_single_rule"].assert_not_called()
    all_mocks["apply_fish_rule"].assert_not_called()


def test_apply_does_not_use_nishio_when_other_rules_succeed(all_mocks, grid):
    all_mocks["apply_single_candidate_rule"].return_value = True

    with patch("rules.nishio_rule.apply_nishio_rule") as mock_nishio:
        apply(grid, include_nishio=True)

    mock_nishio.assert_not_called()


def test_apply_tries_fish_at_all_three_sizes(all_mocks, grid):
    apply(grid, include_nishio=False)

    fish_calls = all_mocks["apply_fish_rule"].call_args_list
    sizes = [call[1]["size"] for call in fish_calls]
    assert sizes == [2, 3, 4]
