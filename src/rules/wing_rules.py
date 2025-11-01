from itertools import combinations
from model import Grid


def apply_xy_wing_rule(grid: Grid) -> bool:
    """Apply the XY-Wing rule to the Sudoku grid.

    Args:
        grid (Grid): The Sudoku grid to apply the solver to.

    Returns:
        bool: True if the solver could be applied, False otherwise.
    """
    applied = False

    # Find an XY-Wing pattern.
    for pivot in [cell for cell in grid if len(cell.candidates) == 2]:
        xy = pivot.candidates

        # Wings must have 2 candidates and share only one with the pivot.
        wings = [
            wing
            for wing in grid.get_neighbours(pivot)
            if len(wing.candidates) == 2 and len(xy.difference(wing.candidates)) == 1
        ]

        for wing1, wing2 in combinations(wings, 2):
            # Reject the wings if they don't share a symmetric difference with the pivot.
            if wing1.candidates.symmetric_difference(wing2.candidates) != xy:
                continue

            # Find a z-value common to both wings.
            z_set = wing1.candidates.intersection(wing2.candidates)
            if len(z_set) != 1:
                continue
            z = z_set.pop()

            # Eliminate z from cells that see both wings of the XY-Wing.
            wing1_neighbours = grid.get_neighbours(wing1)
            wing2_neighbours = grid.get_neighbours(wing2)
            common_neighbours = wing1_neighbours.intersection(wing2_neighbours)

            for cell in [cell for cell in common_neighbours if z in cell.candidates and cell != pivot]:
                cell.candidates -= {z}
                applied = True

    return applied


def apply_xyz_wing_rule(grid: Grid) -> bool:
    """Apply the XYZ-Wing rule to the Sudoku grid.

    Args:
        grid (Grid): The Sudoku grid to apply the solver to.

    Returns:
        bool: True if the solver could be applied, False otherwise.
    """
    applied = False

    # Find an XYZ-Wing pattern.
    for pivot in [cell for cell in grid if len(cell.candidates) == 3]:
        xyz = pivot.candidates

        # Wings must have 2 candidates that are a subset of the pivot's candidates.
        wings = [
            wing
            for wing in grid.get_neighbours(pivot)
            if len(wing.candidates) == 2 and wing.candidates.issubset(xyz)
        ]

        for wing1, wing2 in combinations(wings, 2):
            # Find the z-value common to both wings.
            z_set = wing1.candidates.intersection(wing2.candidates)
            if len(z_set) != 1:
                continue
            z = z_set.pop()

            # Eliminate z from cells that see all three of the XYZ-Wing cells.
            pivot_neighbours = grid.get_neighbours(pivot)
            wing1_neighbours = grid.get_neighbours(wing1)
            wing2_neighbours = grid.get_neighbours(wing2)
            common_neighbours = pivot_neighbours.intersection(wing1_neighbours).intersection(wing2_neighbours)

            for cell in [cell for cell in common_neighbours if z in cell.candidates]:
                cell.candidates -= {z}
                applied = True

    return applied
