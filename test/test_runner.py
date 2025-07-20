from model import Grid
from runner import apply_solver


def test_apply_solver_with_solvable_puzzle_solves_grid():
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

    apply_solver(grid)

    assert all(cell.value is not None for cell in grid)


def test_apply_solver_with_solvable_puzzle_returns_solved_message():
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

    result = apply_solver(grid)

    assert result == "The puzzle was solved!"


def test_apply_solver_with_invalid_grid_returns_illegal_message():
    grid = Grid.from_rows_notation(
        [
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            "123456789",
            "123456789",
        ]
    )

    result = apply_solver(grid)

    assert result == "The input grid contains illegal starting values."


def test_apply_solver_with_unsolvable_puzzle_returns_unsolved_message():
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

    result = apply_solver(grid)

    assert result == (
        "The puzzle could not be solved. Either it's unsolvable or it requires "
        "more advanced techniques than are implemented in this solver."
    )
