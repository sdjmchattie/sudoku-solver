from unittest.mock import patch, MagicMock

from model import Grid, Point
from rules.nishio_rule import apply_nishio_rule


def test_nishio_eliminates_candidate_that_causes_contradiction():
    grid = Grid.from_rows_notation(
        [
            ".23456789",
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

    # Give (0,0) two candidates so nishio has something to test
    grid[Point(0, 0)].candidates = {1, 2}

    mock_instance = MagicMock()
    # First trial is valid, second causes a contradiction
    mock_instance.is_valid.side_effect = [True, False]

    with patch("rules.nishio_rule.Solver", return_value=mock_instance):
        applied = apply_nishio_rule(grid)

    assert applied is True
    # One candidate should have been removed, leaving exactly one
    assert len(grid[Point(0, 0)].candidates) == 1


def test_nishio_returns_false_when_no_contradiction_found():
    grid = Grid.from_rows_notation(
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

    grid[Point(0, 0)].candidates = {1, 2}

    mock_instance = MagicMock()
    # All trials are valid — no contradictions
    mock_instance.is_valid.return_value = True

    with patch("rules.nishio_rule.Solver", return_value=mock_instance):
        applied = apply_nishio_rule(grid)

    assert applied is False


def test_nishio_returns_false_when_grid_is_solved():
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

    assert apply_nishio_rule(grid) is False


def test_nishio_does_not_use_nishio_recursively():
    grid = Grid.from_rows_notation(
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

    grid[Point(0, 0)].candidates = {1, 2}

    mock_instance = MagicMock()
    mock_instance.is_valid.return_value = True

    with patch("rules.nishio_rule.Solver") as mock_solver_class:
        mock_solver_class.return_value = mock_instance
        apply_nishio_rule(grid)

        for solver_call in mock_solver_class.call_args_list:
            _, kwargs = solver_call
            assert kwargs.get("use_nishio") is False


def test_nishio_processes_cells_with_fewest_candidates_first():
    grid = Grid.from_rows_notation(
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

    # Cell (0,0) has 2 candidates, cell (1,0) has 3
    grid[Point(0, 0)].candidates = {1, 2}
    grid[Point(1, 0)].candidates = {1, 2, 3}

    trial_grids = []
    mock_instance = MagicMock()
    mock_instance.is_valid.return_value = True

    original_duplicate = Grid.duplicate

    def capture_duplicate(self):
        dup = original_duplicate(self)
        trial_grids.append(dup)
        return dup

    with (
        patch("rules.nishio_rule.Solver", return_value=mock_instance),
        patch.object(Grid, "duplicate", capture_duplicate),
    ):
        apply_nishio_rule(grid)

    # Cell (0,0) with 2 candidates should be tried first (2 trials),
    # then cell (1,0) with 3 candidates (3 trials)
    assert len(trial_grids) == 5
