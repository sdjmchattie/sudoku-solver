# Sudoku Solver

A Python solver for Sudoku puzzles.
This is part of a blog series where we try to build a tool to solve Sudoku puzzles using the same techniques a human would.

## Prerequisites

This project uses the `uv` package manager [from Astral](https://docs.astral.sh/uv/).
To prepare the dev environment, use the command:

```shell
uv sync
```

## Running the Solver

Prepare your puzzle's initial state using the syntax seen in the `puzzles` directory.
Start the solver by using the command:

```shell
uv run sudoku-solver path/to/your-puzzle.txt
```

## Linting and Testing

Linting code can be done using `./lint.sh`.
Running tests can be done via `uv run pytest`.
