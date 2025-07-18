import argparse
from model import Grid

parser = argparse.ArgumentParser(
    description="A Sudoku solver which applies solving rules just as a human would."
)
parser.add_argument("input", help="The sudoku puzzle to solve.")

args = parser.parse_args()


def run():
    with open(args.input, "r") as f:
        lines = f.readlines()
        grid = Grid.from_rows_notation(lines)

    grid.display()


if __name__ == "__main__":
    run()
