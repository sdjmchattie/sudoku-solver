from .fish_rules import apply_fish_rule
from .hidden_set_rules import (
    apply_hidden_single_rule,
    apply_hidden_pairs_rule,
    apply_hidden_triples_rule,
)
from .locked_candidates_rule import apply_locked_candidates_rule
from .naked_set_rules import apply_naked_pairs_rule, apply_naked_triples_rule
from .single_candidate_rule import apply_single_candidate_rule
from .wing_rules import apply_xy_wing_rule, apply_xyz_wing_rule

__all__ = [
    "apply_fish_rule",
    "apply_hidden_single_rule",
    "apply_hidden_pairs_rule",
    "apply_hidden_triples_rule",
    "apply_locked_candidates_rule",
    "apply_naked_pairs_rule",
    "apply_naked_triples_rule",
    "apply_single_candidate_rule",
    "apply_xy_wing_rule",
    "apply_xyz_wing_rule",
]
