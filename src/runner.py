import argparse
from solver import Solver
from utils import render_grid
from model import Grid

parser = argparse.ArgumentParser(
    description="A Sudoku solver which applies solving rules just as a human would."
)
parser.add_argument("input", help="The sudoku puzzle to solve.")

args = parser.parse_args()


def run():
    with open(args.input, "r") as f:
        input_lines = f.readlines()
        grid = Grid.from_rows_notation(input_lines)

    render_grid(grid).show()
    print(apply_solver(grid))
    render_grid(grid).show()


def apply_solver(grid: Grid) -> str:
    """Apply a Solver to the puzzle defined in the input.

    Args:
        grid (Grid): The Sudoku grid to be solved.

    Returns:
        str: A description of the result of the solving process.
    """
    solver = Solver(grid)

    if not solver.is_valid():
        return "The input grid contains illegal starting values."

    solver.solve()

    if solver.is_solved():
        return "The puzzle was solved!"
    else:
        return (
            "The puzzle could not be solved. Either it's unsolvable or it requires "
            "more advanced techniques than are implemented in this solver."
        )


if __name__ == "__main__":
    run()
