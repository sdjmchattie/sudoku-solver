import pytest
from model.cell import Cell


def test_new_cell_has_no_value():
    cell = Cell()

    assert cell.value is None


def test_new_cell_has_candidates_set():
    cell = Cell()

    assert cell.candidates == set(range(1, 10))


def test_new_cell_value_can_be_set_through_init():
    cell = Cell(5)

    assert cell.value == 5


def test_new_cell_value_can_be_set_through_property():
    cell = Cell()
    cell.value = 3

    assert cell.value == 3


def test_cell_with_value_has_no_candidates():
    cell = Cell(7)

    assert cell.candidates == set()


def test_setting_cell_value_removes_candidates():
    cell = Cell()
    cell.value = 2

    assert cell.candidates == set()


def test_cell_value_cannot_be_set_twice():
    cell = Cell(4)

    with pytest.raises(ValueError) as err:
        cell.value = 5

    assert str(err.value) == "Cannot set value of a cell that already has a value."


def test_cell_value_cannot_be_set_to_zero():
    cell = Cell()

    with pytest.raises(ValueError) as err:
        cell.value = 0

    assert str(err.value) == "Value must be between 1 and 9."


def test_cell_value_cannot_be_set_to_ten():
    cell = Cell()

    with pytest.raises(ValueError) as err:
        cell.value = 10

    assert str(err.value) == "Value must be between 1 and 9."


def test_cell_candidates_can_be_set():
    cell = Cell()
    new_candidates = {1, 2, 3}
    cell.candidates = new_candidates

    assert cell.candidates == new_candidates


def test_cell_candidates_returns_a_copy():
    cell = Cell()
    new_candidates = {1, 2, 3}
    cell.candidates = new_candidates

    assert cell.candidates is not new_candidates


def test_cell_candidates_cannot_be_set_if_value_is_set():
    cell = Cell(5)

    with pytest.raises(ValueError) as err:
        cell.candidates = {1, 2, 3}

    assert (
        str(err.value) == "Cannot set candidates for a cell that already has a value."
    )


def test_cell_candidates_cannot_be_set_with_invalid_value_zero():
    cell = Cell()

    with pytest.raises(ValueError) as err:
        cell.candidates = {0, 1, 2, 3}

    assert str(err.value) == "All candidates must be between 1 and 9."


def test_cell_candidates_cannot_be_set_with_invalid_value_ten():
    cell = Cell()

    with pytest.raises(ValueError) as err:
        cell.candidates = {1, 2, 3, 10}

    assert str(err.value) == "All candidates must be between 1 and 9."
