from model import Grid
from rules import (
    apply_fish_rule,
    apply_hidden_single_rule,
    apply_hidden_pairs_rule,
    apply_hidden_triples_rule,
    apply_locked_candidates_rule,
    apply_naked_pairs_rule,
    apply_naked_triples_rule,
    apply_single_candidate_rule,
    apply_xy_wing_rule,
    apply_xyz_wing_rule,
)


def apply(grid: Grid, include_nishio: bool = True) -> bool:
    """Apply all the rules available, preferring to stop after finding a simple rule to apply.
    If simple rules fail, move on to more and more complex rules.
    Only use Nishio if include_nishio is True.

    Args:
        grid (Grid): The Grid to apply the rules to.
        include_nishio (bool, optional): Use Nishio when all other rules fail to apply. Defaults to True.

    Returns:
        bool: True if any rule changed the grid, False otherwise.
    """
    applied = (
        apply_single_candidate_rule(grid)
        or apply_naked_pairs_rule(grid)
        or apply_naked_triples_rule(grid)
        or apply_hidden_single_rule(grid)
        or apply_hidden_pairs_rule(grid)
        or apply_hidden_triples_rule(grid)
        or apply_locked_candidates_rule(grid)
        or apply_fish_rule(grid, size=2)
        or apply_fish_rule(grid, size=3)
        or apply_fish_rule(grid, size=4)
        or apply_xy_wing_rule(grid)
        or apply_xyz_wing_rule(grid)
    )

    # If no rules were applied, we can try Nishio before giving up.
    # Don't do this if other rules work because it's expensive and a fallback to solve via brute-force.
    if not applied:
        if include_nishio:
            from rules.nishio_rule import apply_nishio_rule

            applied = apply_nishio_rule(grid)

    return applied
