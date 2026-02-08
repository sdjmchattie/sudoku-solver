# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python 3.12+ Sudoku solver that applies human-like solving techniques (no backtracking).
Part of a blog series. Uses `uv` as the package manager.

## Commands

```bash
uv sync                                    # Install dependencies
uv run sudoku-solver path/to/puzzle.txt    # Run solver on a puzzle
uv run pytest                              # Run all tests
uv run pytest tests/rules/test_fish_rules.py          # Run a single test file
uv run pytest tests/rules/test_fish_rules.py -k "swordfish"  # Run specific test
./lint.sh                                  # Lint (mypy + ruff check + ruff format)
```

## Architecture

The solver iteratively applies rules in priority order (simplest first), stopping after the first successful application each cycle, until no rule makes progress.

**Model layer** (`src/model/`): `Point` (frozen dataclass for coordinates), `Cell` (value + candidate set), `Grid` (81 cells with row/column/block querying).

**Rules** (`src/rules/`): Each rule module exports functions with signature `apply_<rule>(grid: Grid, ...) -> bool` returning whether any change was made.
Rules in order of complexity: single candidate → naked sets → hidden sets → locked candidates → fish (X-Wing/Swordfish/Jellyfish) → wings (XY-Wing/XYZ-Wing).

**Solver** (`src/solver.py`): Orchestrates rule application in priority order.

**Runner** (`src/runner.py`): CLI entry point using argparse.
Reads puzzle files (dot notation for empty cells), renders before/after as PNG via Pillow.

## Conventions

- Puzzle files use string notation where `.` = empty cell (see `puzzles/` directory)
- Type hints throughout; validated by mypy in strict-ish mode
- Tests mirror source structure under `tests/`; use pytest parametrize for rule variants
- Grid querying uses set operations on cells (rows, columns, blocks, neighborhoods)
- Markdown content uses newlines between sentences to reduce columns per line
