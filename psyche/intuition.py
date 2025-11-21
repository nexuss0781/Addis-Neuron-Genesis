from dataclasses import dataclass, field
from typing import Dict
from uuid import UUID, uuid4

@dataclass
class IntuitiveBias:
    """A packet of gut feeling."""
    bias_id: UUID = field(default_factory=uuid4)
    targets: Dict[UUID, float] = field(default_factory=dict)
    decay: float = 0.1
    tick: int = 0

    def strength(self, current):
        age = current - self.tick
        return max(0.0, 1.0 - (age * self.decay))

class BiasVector:
    """Physics of feelings."""
    def __init__(self): self.biases = []
    
    def add(self, b): self.biases.append(b)
    
    def net(self, nid, tick):
        val = 0.0
        for b in self.biases:
            if nid in b.targets:
                val += b.strength(tick) * b.targets[nid]
        return min(2.0, val)
