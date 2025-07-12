import pytest
from model.grid import Grid


def test_new_grid_with_none_values_has_empty_cells():
    grid = Grid([[None] * 9] * 9)

    for row in grid._grid:
        for cell in row:
            assert cell.value is None


def test_new_grid_with_values_has_correct_cell_values():
    grid = Grid([list(range(1, 10)) for _ in range(9)])

    for row in grid._grid:
        for i, cell in enumerate(row):
            assert cell.value == i + 1


def test_from_rows_notation_creates_grid_with_correct_values():
    rows = [
        "123456789",
        "987654321",
        "456789123",
        "321654987",
        "654321456",
        "789123654",
        "159753486",
        "753486159",
        "486159753",
    ]
    grid = Grid.from_rows_notation(rows)

    for i, row in enumerate(grid._grid):
        for j, cell in enumerate(row):
            assert cell.value == int(rows[i][j])


def test_from_rows_notation_creates_empty_cells_for_non_numeric():
    rows = [
        ".23456789",
        "9;7654321",
        "45g789123",
        "321@54987",
        "6543)1456",
        "78912 654",
        "159753]86",
        "7534861§9",
        "486159750",
    ]
    grid = Grid.from_rows_notation(rows)

    for i, row in enumerate(grid._grid):
        for j, cell in enumerate(row):
            if i == j:
                assert cell.value is None
            else:
                assert cell.value == int(rows[i][j])


def test_display_prints_full_grid_correctly(capsys):
    rows = [
        "123456789",
        "987654321",
        "456789123",
        "321654987",
        "654321456",
        "789123654",
        "159753486",
        "753486159",
        "486159753",
    ]
    grid = Grid.from_rows_notation(rows)
    grid.display()

    captured = capsys.readouterr()
    expected_output = (
        "+-------+-------+-------+\n"
        "| 1 2 3 | 4 5 6 | 7 8 9 |\n"
        "| 9 8 7 | 6 5 4 | 3 2 1 |\n"
        "| 4 5 6 | 7 8 9 | 1 2 3 |\n"
        "+-------+-------+-------+\n"
        "| 3 2 1 | 6 5 4 | 9 8 7 |\n"
        "| 6 5 4 | 3 2 1 | 4 5 6 |\n"
        "| 7 8 9 | 1 2 3 | 6 5 4 |\n"
        "+-------+-------+-------+\n"
        "| 1 5 9 | 7 5 3 | 4 8 6 |\n"
        "| 7 5 3 | 4 8 6 | 1 5 9 |\n"
        "| 4 8 6 | 1 5 9 | 7 5 3 |\n"
        "+-------+-------+-------+\n"
    )
    assert captured.out == expected_output


def test_display_print_empty_grid_correctly(capsys):
    grid = Grid([[None] * 9] * 9)
    grid.display()

    captured = capsys.readouterr()
    expected_output = (
        "+-------+-------+-------+\n"
        "| . . . | . . . | . . . |\n"
        "| . . . | . . . | . . . |\n"
        "| . . . | . . . | . . . |\n"
        "+-------+-------+-------+\n"
        "| . . . | . . . | . . . |\n"
        "| . . . | . . . | . . . |\n"
        "| . . . | . . . | . . . |\n"
        "+-------+-------+-------+\n"
        "| . . . | . . . | . . . |\n"
        "| . . . | . . . | . . . |\n"
        "| . . . | . . . | . . . |\n"
        "+-------+-------+-------+\n"
    )
    assert captured.out == expected_output


def test_grid_initialization_with_invalid_size_raises_error():
    with pytest.raises(ValueError) as err:
        Grid([[None] * 8] * 9)  # Invalid row size
    assert str(err.value) == "Grid must be 9x9."

    with pytest.raises(ValueError) as err:
        Grid([[None] * 9] * 8)  # Invalid column size
    assert str(err.value) == "Grid must be 9x9."

    with pytest.raises(ValueError) as err:
        Grid([[None] * 10] * 9)  # Too many columns
    assert str(err.value) == "Grid must be 9x9."

    with pytest.raises(ValueError) as err:
        Grid([[None] * 9] * 10)  # Too many rows
    assert str(err.value) == "Grid must be 9x9."

    with pytest.raises(ValueError) as err:
        Grid.from_rows_notation(["123456789"] * 8)  # Invalid row count
    assert str(err.value) == "Grid must be 9x9."
