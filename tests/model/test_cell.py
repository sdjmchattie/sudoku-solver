import pytest
from model.cell import Cell
from model.point import Point


@pytest.fixture
def coord():
    return Point(0, 0)


@pytest.fixture
def block():
    return Point(1, 1)


@pytest.fixture
def coord_in_block():
    return Point(2, 2)


def test_cell_coord_is_stored():
    cell = Cell(coord, block, coord_in_block)

    assert cell.coord is coord


def test_cell_coord_cannot_be_set_after_creation():
    cell = Cell(coord, block, coord_in_block)

    with pytest.raises(AttributeError):
        cell.coord = Point(1, 1)  # Attempt to change coord


def test_cell_block_is_stored():
    cell = Cell(coord, block, coord_in_block)

    assert cell.block is block


def test_cell_block_cannot_be_set_after_creation():
    cell = Cell(coord, block, coord_in_block)

    with pytest.raises(AttributeError):
        cell.block = Point(1, 1)  # Attempt to change coord


def test_cell_coord_in_block_is_stored():
    cell = Cell(coord, block, coord_in_block)

    assert cell.coord_in_block is coord_in_block


def test_cell_coord_in_block_cannot_be_set_after_creation():
    cell = Cell(coord, block, coord_in_block)

    with pytest.raises(AttributeError):
        cell.coord_in_block = Point(1, 1)  # Attempt to change coord


def test_new_cell_has_no_value():
    cell = Cell(coord, block, coord_in_block)

    assert cell.value is None


def test_new_cell_has_candidates_set():
    cell = Cell(coord, block, coord_in_block)

    assert cell.candidates == set(range(1, 10))


def test_new_cell_value_can_be_set_through_init():
    cell = Cell(coord, block, coord_in_block, 5)

    assert cell.value == 5


def test_new_cell_value_can_be_set_through_property():
    cell = Cell(coord, block, coord_in_block)
    cell.value = 3

    assert cell.value == 3


def test_cell_with_value_has_no_candidates():
    cell = Cell(coord, block, coord_in_block, 7)

    assert cell.candidates == set()


def test_setting_cell_value_removes_candidates():
    cell = Cell(coord, block, coord_in_block)
    cell.value = 2

    assert cell.candidates == set()


def test_cell_value_cannot_be_set_twice():
    cell = Cell(coord, block, coord_in_block, 4)

    with pytest.raises(ValueError) as err:
        cell.value = 5

    assert str(err.value) == "Cannot set value of a cell that already has a value."


def test_cell_value_cannot_be_set_to_zero():
    cell = Cell(coord, block, coord_in_block)

    with pytest.raises(ValueError) as err:
        cell.value = 0

    assert str(err.value) == "Value must be between 1 and 9."


def test_cell_value_cannot_be_set_to_ten():
    cell = Cell(coord, block, coord_in_block)

    with pytest.raises(ValueError) as err:
        cell.value = 10

    assert str(err.value) == "Value must be between 1 and 9."


def test_cell_candidates_can_be_set():
    cell = Cell(coord, block, coord_in_block)
    new_candidates = {1, 2, 3}
    cell.candidates = new_candidates

    assert cell.candidates == new_candidates


def test_cell_candidates_returns_a_copy():
    cell = Cell(coord, block, coord_in_block)
    new_candidates = {1, 2, 3}
    cell.candidates = new_candidates

    assert cell.candidates is not new_candidates


def test_cell_candidates_cannot_be_set_if_value_is_set():
    cell = Cell(coord, block, coord_in_block, 5)

    with pytest.raises(ValueError) as err:
        cell.candidates = {1, 2, 3}

    assert (
        str(err.value) == "Cannot set candidates for a cell that already has a value."
    )


def test_cell_candidates_cannot_be_set_with_invalid_value_zero():
    cell = Cell(coord, block, coord_in_block)

    with pytest.raises(ValueError) as err:
        cell.candidates = {0, 1, 2, 3}

    assert str(err.value) == "All candidates must be between 1 and 9."


def test_cell_candidates_cannot_be_set_with_invalid_value_ten():
    cell = Cell(coord, block, coord_in_block)

    with pytest.raises(ValueError) as err:
        cell.candidates = {1, 2, 3, 10}

    assert str(err.value) == "All candidates must be between 1 and 9."
