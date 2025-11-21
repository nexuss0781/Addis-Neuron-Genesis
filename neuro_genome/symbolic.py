import math
from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class SymbolicVector:
    """
    A 5-Dimensional Vector representing location in Meaning Space.
    """
    creation_destruction: float
    order_chaos: float
    self_other: float
    light_dark: float
    stasis_change: float

    def to_dict(self) -> Dict[str, float]:
        return {
            "creation_destruction": self.creation_destruction,
            "order_chaos": self.order_chaos,
            "self_other": self.self_other,
            "light_dark": self.light_dark,
            "stasis_change": self.stasis_change
        }

    @staticmethod
    def from_dict(data: Dict[str, float]) -> 'SymbolicVector':
        return SymbolicVector(
            creation_destruction=data.get("creation_destruction", 0.0),
            order_chaos=data.get("order_chaos", 0.0),
            self_other=data.get("self_other", 0.0),
            light_dark=data.get("light_dark", 0.0),
            stasis_change=data.get("stasis_change", 0.0)
        )

# The Prime Seeds of Meaning
VECTOR_SEEDS = {
    "sun": SymbolicVector(0.8, 0.5, 0.0, 1.0, 0.1),
    "star": SymbolicVector(0.5, 0.2, 0.0, 0.9, 0.1),
    "earth": SymbolicVector(0.9, 0.5, 0.0, 0.0, 0.2),
    "life": SymbolicVector(1.0, -0.2, 0.5, 0.5, -0.8),
    "death": SymbolicVector(-1.0, 0.5, -0.5, -1.0, 1.0),
    "hero": SymbolicVector(0.5, -0.5, 0.8, 0.5, -0.9),
    "shadow": SymbolicVector(-0.8, -0.9, 0.0, -0.9, -0.5),
    "learn": SymbolicVector(0.5, 0.5, 0.5, 0.8, -0.5),
    "create": SymbolicVector(1.0, -0.5, 0.2, 0.5, -1.0),
    "destroy": SymbolicVector(-1.0, -1.0, 0.0, -1.0, 1.0),
}
