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


def test_iteration_over_grid_cells():
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

    cells = list(grid)
    assert len(cells) == 81

    for i, (row, col, cell) in enumerate(cells):
        assert cell.value == int(rows[row][col])
        assert row == i // 9
        assert col == i % 9

def test_indexing_grid_cells():
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

    for row in range(9):
        for col in range(9):
            assert grid[row, col].value == int(rows[row][col])


def test_indexing_invalid_cells_raises_error():
    grid = Grid([[None] * 9] * 9)

    with pytest.raises(IndexError):
        _ = grid[9, 0]  # Row index out of bounds

    with pytest.raises(IndexError):
        _ = grid[0, 9]  # Column index out of bounds

    with pytest.raises(IndexError):
        _ = grid[-1, 0]  # Negative row index

    with pytest.raises(IndexError):
        _ = grid[0, -1]  # Negative column index


def test_get_neighbours():
    rows = [
        "999199999",
        "999199999",
        "999199999",
        "999111999",
        "111511111",
        "999111999",
        "999199999",
        "999199999",
        "999199999",
    ]
    grid = Grid.from_rows_notation(rows)

    # Test the cell at [4, 3]
    neighbours = grid.get_neighbours(4, 3)
    assert len(neighbours) == 20
    assert all([cell.value == 1 for cell in neighbours]), "Values should all be 1 for neighbours of [4, 3]"


def test_get_neightbours_with_invalid_indices():
    grid = Grid([[None] * 9] * 9)

    with pytest.raises(IndexError):
        _ = grid.get_neighbours(9, 0)  # Row index out of bounds

    with pytest.raises(IndexError):
        _ = grid.get_neighbours(0, 9)  # Column index out of bounds

    with pytest.raises(IndexError):
        _ = grid.get_neighbours(-1, 0)  # Negative row index

    with pytest.raises(IndexError):
        _ = grid.get_neighbours(0, -1)  # Negative column index


def test_get_block_neighbours():
    rows = [
        "511999999",
        "111999999",
        "111999999",
        "999222999",
        "999252999",
        "999222999",
        "999999333",
        "999999333",
        "999999335",
    ]
    grid = Grid.from_rows_notation(rows)

    # Test a cell in the top-left block
    neighbours = grid.get_block_neighbours(0, 0)
    assert len(neighbours) == 8
    assert all([cell.value == 1 for cell in neighbours]), "Values should all be 1 in the top-left block"

    # Test a cell in the center block
    neighbours = grid.get_block_neighbours(4, 4)
    assert len(neighbours) == 8
    assert all([cell.value == 2 for cell in neighbours]), "Values should all be 2 in the center block"

    # Test a cell in the bottom-right block
    neighbours = grid.get_block_neighbours(8, 8)
    assert len(neighbours) == 8
    assert all([cell.value == 3 for cell in neighbours]), "Values should all be 3 in the bottom-right block"


def test_get_block_neightbours_with_invalid_indices():
    grid = Grid([[None] * 9] * 9)

    with pytest.raises(IndexError):
        _ = grid.get_block_neighbours(9, 0)  # Row index out of bounds

    with pytest.raises(IndexError):
        _ = grid.get_block_neighbours(0, 9)  # Column index out of bounds

    with pytest.raises(IndexError):
        _ = grid.get_block_neighbours(-1, 0)  # Negative row index

    with pytest.raises(IndexError):
        _ = grid.get_block_neighbours(0, -1)  # Negative column index


def test_get_col_neighbours():
    rows = [
        "599929993",
        "199929993",
        "199929993",
        "199929993",
        "199959993",
        "199929993",
        "199929993",
        "199929993",
        "199929995",
    ]
    grid = Grid.from_rows_notation(rows)

    # Test a cell in column 0
    neighbours = grid.get_col_neighbours(0, 0)
    assert len(neighbours) == 8
    assert all([cell.value == 1 for cell in neighbours]), "Values should all be 1 in column 0"

    # Test a cell in column 4
    neighbours = grid.get_col_neighbours(4, 4)
    assert len(neighbours) == 8
    assert all([cell.value == 2 for cell in neighbours]), "Values should all be 2 in column 4"

    # Test a cell in column 8
    neighbours = grid.get_col_neighbours(8, 8)
    assert len(neighbours) == 8
    assert all([cell.value == 3 for cell in neighbours]), "Values should all be 3 in column 8"


def test_get_col_neightbours_with_invalid_indices():
    grid = Grid([[None] * 9] * 9)

    with pytest.raises(IndexError):
        _ = grid.get_col_neighbours(9, 0)  # Row index out of bounds

    with pytest.raises(IndexError):
        _ = grid.get_col_neighbours(0, 9)  # Column index out of bounds

    with pytest.raises(IndexError):
        _ = grid.get_col_neighbours(-1, 0)  # Negative row index

    with pytest.raises(IndexError):
        _ = grid.get_col_neighbours(0, -1)  # Negative column index


def test_get_row_neighbours():
    rows = [
        "511111111",
        "999999999",
        "999999999",
        "999999999",
        "222252222",
        "999999999",
        "999999999",
        "999999999",
        "333333335",
    ]
    grid = Grid.from_rows_notation(rows)

    # Test a cell in row 0
    neighbours = grid.get_row_neighbours(0, 0)
    assert len(neighbours) == 8
    assert all([cell.value == 1 for cell in neighbours]), "Values should all be 1 in row 0"

    # Test a cell in row 4
    neighbours = grid.get_row_neighbours(4, 4)
    assert len(neighbours) == 8
    assert all([cell.value == 2 for cell in neighbours]), "Values should all be 2 in row 4"

    # Test a cell in row 8
    neighbours = grid.get_row_neighbours(8, 8)
    assert len(neighbours) == 8
    assert all([cell.value == 3 for cell in neighbours]), "Values should all be 3 in row 8"


def test_get_row_neightbours_with_invalid_indices():
    grid = Grid([[None] * 9] * 9)

    with pytest.raises(IndexError):
        _ = grid.get_row_neighbours(9, 0)  # Row index out of bounds

    with pytest.raises(IndexError):
        _ = grid.get_row_neighbours(0, 9)  # Column index out of bounds

    with pytest.raises(IndexError):
        _ = grid.get_row_neighbours(-1, 0)  # Negative row index

    with pytest.raises(IndexError):
        _ = grid.get_row_neighbours(0, -1)  # Negative column index
