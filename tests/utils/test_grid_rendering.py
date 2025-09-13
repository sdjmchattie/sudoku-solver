from model.grid import Grid
from utils import display_grid
from utils.grid_rendering import render_grid
from PIL.Image import Image


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
    display_grid(grid)

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
    display_grid(grid)

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


# Tests for render_grid are more complex due to the image output.
# Let's just test that an image was returned with the right size and mode.


def test_render_grid_returns_image():
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
    img = render_grid(grid)

    assert isinstance(img, Image)
    assert img.size == (470, 470)  # Check the size of the image
    assert img.mode == "RGB"  # Check the color mode


def test_render_grid_empty_grid():
    grid = Grid([[None] * 9] * 9)
    img = render_grid(grid)

    assert isinstance(img, Image)
    assert img.size == (470, 470)  # Check the size of the image
    assert img.mode == "RGB"  # Check the color mode
