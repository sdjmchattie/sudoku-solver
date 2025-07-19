from model.point import Point
from PIL import Image, ImageDraw, ImageFont


def display_grid(grid):
    """
    Display the grid in a human-readable format directly to standard output.
    """
    for row_index in range(1, 10):
        if row_index % 3 == 1:
            print("+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+")

        for col_index in range(1, 10):
            if col_index % 3 == 1:
                print("|", end=" ")

            cell = grid[Point(col_index - 1, row_index - 1)]
            print(cell.value or ".", end=" ")

        print("|")

    print("+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+")


def render_grid(grid):
    """
    Get a PNG version of the grid.
    """
    # Create a blank image with white background
    img = Image.new("RGB", (470, 470), "white")
    draw = ImageDraw.Draw(img)

    # Draw grid lines
    for i in range(0, 10):
        line_width = 3 if i % 3 == 0 else 1
        draw.line((10 + i * 50, 10, 10 + i * 50, 460), fill="black", width=line_width)
        draw.line((10, 10 + i * 50, 460, 10 + i * 50), fill="black", width=line_width)

    # Draw numbers
    small_font = ImageFont.load_default(12.0)
    large_font = ImageFont.load_default(30.0)
    for cell in grid:
        x = (cell.coord.x * 50) + 26
        y = (cell.coord.y * 50) + 15

        if cell.value is not None:
            draw.text(
                (x, y), str(cell.value), fill="black", font=large_font, align="center"
            )
        else:
            for candidate in cell.candidates:
                candidate_x = x - 6 + (candidate - 1) % 3 * 12
                candidate_y = y + (candidate - 1) // 3 * 14
                draw.text(
                    (candidate_x, candidate_y),
                    str(candidate),
                    fill="blue",
                    font=small_font,
                    align="center",
                )

    return img
