import pytest
from model.grid import Grid
from model.point import Point


def test_new_grid_with_none_values_has_empty_cells():
    grid = Grid([[None] * 9] * 9)

    assert len(grid._grid) == 81

    for cell in grid._grid:
        assert cell.value is None


def test_new_grid_with_values_has_stored_values():
    grid = Grid([list(range(1, 10)) for _ in range(9)])

    assert len(grid._grid) == 81

    seen_values = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    for cell in grid._grid:
        seen_values[cell.value] += 1

    for i in range(1, 10):
        assert seen_values[i] == 9, f"Value {i} should appear 9 times in the grid."


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

    for cell in grid._grid:
        assert cell.value == int(rows[cell.coord.y][cell.coord.x]), (
            f"Cell at {cell.coord} should have value {int(rows[cell.coord.y][cell.coord.x])}"
        )


def test_from_rows_notation_creates_empty_cells_for_invalid_values():
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

    for cell in grid._grid:
        if cell.coord.x == cell.coord.y:
            assert cell.value is None, (
                f"Cell at {cell.coord} should be empty, but has value {cell.value}"
            )


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


def test_new_grid_sets_initial_candidates_correctly():
    rows = [
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
    grid = Grid.from_rows_notation(rows)

    assert grid[Point(0, 0)].candidates == {5, 6}, (
        "Cell (0, 0) should have candidates {5, 6}"
    )
    assert grid[Point(2, 0)].candidates == {5}, "Cell (2, 0) should have candidates {5}"
    assert grid[Point(4, 0)].candidates == {9, 5, 6}, (
        "Cell (4, 0) should have candidates {9, 5, 6}"
    )
    assert grid[Point(6, 0)].candidates == {9, 4, 6}, (
        "Cell (6, 0) should have candidates {9, 4, 6}"
    )
    assert grid[Point(2, 1)].candidates == {1, 2, 5}, (
        "Cell (2, 1) should have candidates {1, 2, 5}"
    )
    assert grid[Point(4, 1)].candidates == {9, 5, 6}, (
        "Cell (4, 1) should have candidates {9, 5, 6}"
    )
    assert grid[Point(6, 1)].candidates == {9, 6}, (
        "Cell (6, 1) should have candidates {9, 6}"
    )
    assert grid[Point(7, 1)].candidates == {9, 2}, (
        "Cell (7, 1) should have candidates {9, 2}"
    )
    assert grid[Point(8, 1)].candidates == {9, 2}, (
        "Cell (8, 1) should have candidates {9, 2}"
    )
    assert grid[Point(1, 2)].candidates == {1, 2, 6}, (
        "Cell (1, 2) should have candidates {1, 2, 6}"
    )
    assert grid[Point(3, 2)].candidates == {1, 6}, (
        "Cell (3, 2) should have candidates {1, 6}"
    )
    assert grid[Point(4, 2)].candidates == {6}, "Cell (4, 2) should have candidates {6}"
    assert grid[Point(0, 3)].candidates == {1, 2, 5}, (
        "Cell (0, 3) should have candidates {1, 2, 5}"
    )
    assert grid[Point(5, 3)].candidates == {1, 5}, (
        "Cell (5, 3) should have candidates {1, 5}"
    )
    assert grid[Point(6, 3)].candidates == {9}, "Cell (6, 3) should have candidates {9}"
    assert grid[Point(7, 3)].candidates == {9, 2}, (
        "Cell (7, 3) should have candidates {9, 2}"
    )
    assert grid[Point(2, 4)].candidates == {1, 2}, (
        "Cell (2, 4) should have candidates {1, 2}"
    )
    assert grid[Point(3, 4)].candidates == {1, 4}, (
        "Cell (3, 4) should have candidates {1, 4}"
    )
    assert grid[Point(5, 4)].candidates == {1}, "Cell (5, 4) should have candidates {1}"
    assert grid[Point(8, 4)].candidates == {2, 4, 7}, (
        "Cell (8, 4) should have candidates {2, 4, 7}"
    )
    assert grid[Point(0, 5)].candidates == {5}, "Cell (0, 5) should have candidates {5}"
    assert grid[Point(1, 5)].candidates == {3}, "Cell (1, 5) should have candidates {3}"
    assert grid[Point(5, 5)].candidates == {5, 6}, (
        "Cell (5, 5) should have candidates {5, 6}"
    )
    assert grid[Point(8, 5)].candidates == {4}, "Cell (8, 5) should have candidates {4}"
    assert grid[Point(3, 6)].candidates == {6}, "Cell (3, 6) should have candidates {6}"
    assert grid[Point(6, 6)].candidates == {9, 3}, (
        "Cell (6, 6) should have candidates {9, 3}"
    )
    assert grid[Point(7, 6)].candidates == {8, 9}, (
        "Cell (7, 6) should have candidates {8, 9}"
    )
    assert grid[Point(8, 6)].candidates == {9}, "Cell (8, 6) should have candidates {9}"
    assert grid[Point(0, 7)].candidates == {2, 6}, (
        "Cell (0, 7) should have candidates {2, 6}"
    )
    assert grid[Point(1, 7)].candidates == {2, 6}, (
        "Cell (1, 7) should have candidates {2, 6}"
    )
    assert grid[Point(2, 7)].candidates == {9, 2}, (
        "Cell (2, 7) should have candidates {9, 2}"
    )
    assert grid[Point(4, 7)].candidates == {8, 9, 6}, (
        "Cell (4, 7) should have candidates {8, 9, 6}"
    )
    assert grid[Point(1, 8)].candidates == {1}, "Cell (1, 8) should have candidates {1}"
    assert grid[Point(3, 8)].candidates == {5}, "Cell (3, 8) should have candidates {5}"
    assert grid[Point(5, 8)].candidates == {9, 5}, (
        "Cell (5, 8) should have candidates {9, 5}"
    )
    assert grid[Point(7, 8)].candidates == {9, 7}, (
        "Cell (7, 8) should have candidates {9, 7}"
    )


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

    for cell in grid:
        assert cell.value == int(rows[cell.coord.y][cell.coord.x]), (
            f"Cell at {cell.coord} should have value {int(rows[cell.coord.y][cell.coord.x])}"
        )


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
            assert grid[Point(col, row)].value == int(rows[row][col]), (
                f"Cell at ({col}, {row}) should have value {int(rows[row][col])}"
            )


def test_indexing_invalid_cells_returns_none():
    grid = Grid([[None] * 9] * 9)

    assert grid[Point(0, 9)] is None  # Row index out of bounds
    assert grid[Point(9, 0)] is None  # Column index out of bounds
    assert grid[Point(0, -1)] is None  # Negative row index
    assert grid[Point(-1, 0)] is None  # Negative column index


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

    cell = grid[Point(3, 4)]
    neighbours = grid.get_neighbours(cell)
    assert len(neighbours) == 20
    print(f"Neighbours of {cell.coord}: {[n.value for n in neighbours]}")
    assert all([cell.value == 1 for cell in neighbours]), (
        "Values should all be 1 for neighbours of [3, 4]"
    )


def test_get_neighbours_with_invalid_indices():
    grid = Grid([[None] * 9] * 9)

    with pytest.raises(ValueError):
        _ = grid.get_neighbours(grid[Point(9, 0)])  # Row index out of bounds

    with pytest.raises(ValueError):
        _ = grid.get_neighbours(grid[Point(0, 9)])  # Column index out of bounds

    with pytest.raises(ValueError):
        _ = grid.get_neighbours(grid[Point(0, -1)])  # Negative row index

    with pytest.raises(ValueError):
        _ = grid.get_neighbours(grid[Point(-1, 0)])  # Negative column index


def test_get_block_cells():
    rows = [
        "111999999",
        "111999999",
        "111999999",
        "999222999",
        "999222999",
        "999222999",
        "999999333",
        "999999333",
        "999999333",
    ]
    grid = Grid.from_rows_notation(rows)

    # Test a cell in the top-left block
    block = grid.get_block_cells(Point(0, 0))
    assert len(block) == 9
    assert all([cell.value == 1 for cell in block]), (
        "Values should all be 1 in the top-left block"
    )

    # Test a cell in the center block
    block = grid.get_block_cells(Point(1, 1))
    assert len(block) == 9
    assert all([cell.value == 2 for cell in block]), (
        "Values should all be 2 in the center block"
    )

    # Test a cell in the bottom-right block
    block = grid.get_block_cells(Point(2, 2))
    assert len(block) == 9
    assert all([cell.value == 3 for cell in block]), (
        "Values should all be 3 in the bottom-right block"
    )


def test_get_block_cells_with_invalid_coordinates():
    grid = Grid([[None] * 9] * 9)

    assert len(grid.get_block_cells(Point(3, 0))) == 0  # Block x coordinate too high
    assert len(grid.get_block_cells(Point(0, 3))) == 0  # Block y coordinate too high
    assert len(grid.get_block_cells(Point(-1, 0))) == 0  # Block x coordinate too low
    assert len(grid.get_block_cells(Point(0, -1))) == 0  # Block x coordinate too low


def test_get_column_cells_no_block():
    rows = [
        "199929993",
        "199929993",
        "199929993",
        "199929993",
        "199929993",
        "199929993",
        "199929993",
        "199929993",
        "199929993",
    ]
    grid = Grid.from_rows_notation(rows)

    # Test column 0
    column = grid.get_column_cells(0)
    assert len(column) == 9
    assert all([cell.value == 1 for cell in column]), (
        "Values should all be 1 in column 0"
    )

    # Test column 4
    column = grid.get_column_cells(4)
    assert len(column) == 9
    assert all([cell.value == 2 for cell in column]), (
        "Values should all be 2 in column 4"
    )

    # Test column 8
    column = grid.get_column_cells(8)
    assert len(column) == 9
    assert all([cell.value == 3 for cell in column]), (
        "Values should all be 3 in column 8"
    )


def test_get_column_cells_in_block():
    rows = [
        "299939995",
        "299939995",
        "299939995",
        "199949995",
        "199949995",
        "199949995",
        "199939996",
        "199939996",
        "199939996",
    ]
    grid = Grid.from_rows_notation(rows)

    # Test column 0 top-left block
    column = grid.get_column_cells(0, 0)
    assert len(column) == 3
    assert all([cell.value == 2 for cell in column]), (
        "Values should all be 2 in column 0"
    )

    # Test column 4 centre block
    column = grid.get_column_cells(4, 1)
    assert len(column) == 3
    assert all([cell.value == 4 for cell in column]), (
        "Values should all be 4 in column 4"
    )

    # Test column 8 bottom-right block
    column = grid.get_column_cells(8, 2)
    assert len(column) == 3
    assert all([cell.value == 6 for cell in column]), (
        "Values should all be 6 in column 8"
    )


def test_get_column_cells_with_invalid_index():
    grid = Grid([[None] * 9] * 9)

    assert len(grid.get_column_cells(9)) == 0  # Column index too high
    assert len(grid.get_column_cells(-1)) == 0  # Column index too low


def test_get_column_cells_with_invalid_block():
    grid = Grid([[None] * 9] * 9)

    assert len(grid.get_column_cells(0, 3)) == 0  # Block index too high
    assert len(grid.get_column_cells(0, -1)) == 0  # Block index too low


def test_get_row_cells_no_block():
    rows = [
        "111111111",
        "999999999",
        "999999999",
        "999999999",
        "222222222",
        "999999999",
        "999999999",
        "999999999",
        "333333333",
    ]
    grid = Grid.from_rows_notation(rows)

    # Test a cell in row 0
    row = grid.get_row_cells(0)
    assert len(row) == 9
    assert all([cell.value == 1 for cell in row]), "Values should all be 1 in row 0"

    # Test a cell in row 4
    row = grid.get_row_cells(4)
    assert len(row) == 9
    assert all([cell.value == 2 for cell in row]), "Values should all be 2 in row 4"

    # Test a cell in row 8
    row = grid.get_row_cells(8)
    assert len(row) == 9
    assert all([cell.value == 3 for cell in row]), "Values should all be 3 in row 8"


def test_get_row_cells_in_block():
    rows = [
        "222111111",
        "999999999",
        "999999999",
        "999999999",
        "333444333",
        "999999999",
        "999999999",
        "999999999",
        "555555666",
    ]
    grid = Grid.from_rows_notation(rows)

    # Test row 0 top-left block
    row = grid.get_row_cells(0, 0)
    assert len(row) == 3
    assert all([cell.value == 2 for cell in row]), "Values should all be 2 in row 0"

    # Test row 4 centre block
    row = grid.get_row_cells(4, 1)
    assert len(row) == 3
    assert all([cell.value == 4 for cell in row]), "Values should all be 4 in row 4"

    # Test row 8 bottom-right block
    row = grid.get_row_cells(8, 2)
    assert len(row) == 3
    assert all([cell.value == 6 for cell in row]), "Values should all be 6 in row 8"


def test_get_row_cells_with_invalid_row_index():
    grid = Grid([[None] * 9] * 9)

    assert len(grid.get_row_cells(9)) == 0  # Row index too high
    assert len(grid.get_row_cells(-1)) == 0  # Row index too low


def test_get_row_cells_with_invalid_block_index():
    grid = Grid([[None] * 9] * 9)

    assert len(grid.get_row_cells(0, 3)) == 0  # Block index too high
    assert len(grid.get_row_cells(0, -1)) == 0  # Block index too low
