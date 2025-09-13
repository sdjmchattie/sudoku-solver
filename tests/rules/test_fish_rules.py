from model import Grid, Point
from rules.fish_rules import apply_fish_rule

# Note that in these tests the candidates are forced on the cells
# to ensure that the rules can be applied. In a real Sudoku puzzle,
# candidates would be determined by the puzzle's initial state.


class TestXWingRules:
    def test_fish_in_rows_removes_col_candidates(self):
        grid = Grid.from_rows_notation(["." * 9] * 9)

        # Set candidates for an X-Wing on rows 3 and 5 with candidate 8.
        for y in [3, 5]:
            for x in range(9):
                if x not in [2, 7]:
                    grid[Point(x, y)].candidates -= {8}

        apply_fish_rule(grid, size=2)

        # Candidate 8 should no longer be in other rows of columns 2 and 7.
        for x in [2, 7]:
            for y in range(9):
                if y not in [3, 5]:
                    assert 8 not in grid[Point(x, y)].candidates

    def test_fish_in_cols_removes_row_candidates(self):
        grid = Grid.from_rows_notation(["." * 9] * 9)

        # Set candidates for an X-Wing on columns 3 and 5 with candidate 8.
        for x in [3, 5]:
            for y in range(9):
                if y not in [2, 7]:
                    grid[Point(x, y)].candidates -= {8}

        apply_fish_rule(grid, size=2)

        # Candidate 8 should no longer be in other columns of rows 2 and 7.
        for y in [2, 7]:
            for x in range(9):
                if x not in [3, 5]:
                    assert 8 not in grid[Point(x, y)].candidates

    def test_returns_true_when_able_to_update_candidates(self):
        grid = Grid.from_rows_notation(["." * 9] * 9)

        # Set candidates for an X-Wing on rows 3 and 5 with candidate 8.
        for y in [3, 5]:
            for x in range(9):
                if x not in [2, 7]:
                    grid[Point(x, y)].candidates -= {8}

        assert apply_fish_rule(grid, size=2) is True

    def test_returns_false_when_unable_to_update_candidates(self):
        grid = Grid.from_rows_notation(["." * 9] * 9)

        assert apply_fish_rule(grid, size=2) is False

    def test_apply_locked_candidates_rule_returns_false_when_grid_is_complete(self):
        grid = Grid.from_rows_notation(
            [
                "123456789",
                "456789123",
                "789123456",
                "234567891",
                "567891234",
                "891234567",
                "345678912",
                "678912345",
                "912345678",
            ]
        )

        assert apply_fish_rule(grid, size=2) is False


class TestSwordfishRules:
    def test_fish_in_rows_removes_col_candidates(self):
        grid = Grid.from_rows_notation(["." * 9] * 9)

        # Set candidates for a swordfish on rows 3, 5 and 8 with candidate 8.
        for y in [3, 5, 8]:
            for x in range(9):
                if x not in [2, 4, 7]:
                    grid[Point(x, y)].candidates -= {8}

        apply_fish_rule(grid, size=3)

        # Candidate 8 should no longer be in other rows of columns 2, 4 and 7.
        for x in [2, 4, 7]:
            for y in range(9):
                if y not in [3, 5, 8]:
                    assert 8 not in grid[Point(x, y)].candidates

    def test_fish_in_cols_removes_row_candidates(self):
        grid = Grid.from_rows_notation(["." * 9] * 9)

        # Set candidates for a swordfish on columns 3, 5 and 8 with candidate 8.
        for x in [3, 5, 8]:
            for y in range(9):
                if y not in [2, 4, 7]:
                    grid[Point(x, y)].candidates -= {8}

        apply_fish_rule(grid, size=3)

        # Candidate 8 should no longer be in other columns of rows 2, 4 and 7.
        for y in [2, 4, 7]:
            for x in range(9):
                if x not in [3, 5, 8]:
                    assert 8 not in grid[Point(x, y)].candidates

    def test_returns_true_when_able_to_update_candidates(self):
        grid = Grid.from_rows_notation(["." * 9] * 9)

        # Set candidates for a swordfish on rows 3, 5 and 8 with candidate 8.
        for y in [3, 5, 8]:
            for x in range(9):
                if x not in [2, 4, 7]:
                    grid[Point(x, y)].candidates -= {8}

        assert apply_fish_rule(grid, size=3) is True

    def test_returns_false_when_unable_to_update_candidates(self):
        grid = Grid.from_rows_notation(["." * 9] * 9)

        assert apply_fish_rule(grid, size=3) is False

    def test_apply_locked_candidates_rule_returns_false_when_grid_is_complete(self):
        grid = Grid.from_rows_notation(
            [
                "123456789",
                "456789123",
                "789123456",
                "234567891",
                "567891234",
                "891234567",
                "345678912",
                "678912345",
                "912345678",
            ]
        )

        assert apply_fish_rule(grid, size=3) is False


class TestJellyfishRules:
    def test_fish_in_rows_removes_col_candidates(self):
        grid = Grid.from_rows_notation(["." * 9] * 9)

        # Set candidates for a jellyfish on rows 1, 3, 5 and 7 with candidate 8.
        for y in [1, 3, 5, 7]:
            for x in range(9):
                if x not in [2, 4, 6, 8]:
                    grid[Point(x, y)].candidates -= {8}

        apply_fish_rule(grid, size=4)

        # Candidate 8 should no longer be in other rows of columns 2, 4, 6 and 8.
        for x in [2, 4, 6, 8]:
            for y in range(9):
                if y not in [1, 3, 5, 7]:
                    assert 8 not in grid[Point(x, y)].candidates

    def test_fish_in_cols_removes_row_candidates(self):
        grid = Grid.from_rows_notation(["." * 9] * 9)

        # Set candidates for a jellyfish on columns 1, 3, 5 and 7 with candidate 8.
        for x in [1, 3, 5, 7]:
            for y in range(9):
                if y not in [2, 4, 6, 8]:
                    grid[Point(x, y)].candidates -= {8}

        apply_fish_rule(grid, size=4)

        # Candidate 8 should no longer be in other columns of rows 2, 4, 6 and 8.
        for y in [2, 4, 6, 8]:
            for x in range(9):
                if x not in [1, 3, 5, 7]:
                    assert 8 not in grid[Point(x, y)].candidates

    def test_returns_true_when_able_to_update_candidates(self):
        grid = Grid.from_rows_notation(["." * 9] * 9)

        # Set candidates for a jellyfish on rows 1, 3, 5 and 7 with candidate 8.
        for y in [1, 3, 5, 7]:
            for x in range(9):
                if x not in [2, 4, 6, 8]:
                    grid[Point(x, y)].candidates -= {8}

        assert apply_fish_rule(grid, size=4) is True

    def test_returns_false_when_unable_to_update_candidates(self):
        grid = Grid.from_rows_notation(["." * 9] * 9)

        assert apply_fish_rule(grid, size=4) is False

    def test_apply_locked_candidates_rule_returns_false_when_grid_is_complete(self):
        grid = Grid.from_rows_notation(
            [
                "123456789",
                "456789123",
                "789123456",
                "234567891",
                "567891234",
                "891234567",
                "345678912",
                "678912345",
                "912345678",
            ]
        )

        assert apply_fish_rule(grid, size=4) is False
