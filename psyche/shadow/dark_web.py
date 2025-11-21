from dataclasses import dataclass
from typing import Dict
from uuid import UUID
from neuro_genome.schemas import ResonanceNeuron

@dataclass
class ShadowNeuron(ResonanceNeuron):
    is_shadow: bool = True
    corruption: float = 0.0

class DarkWeb:
    """The hidden graph."""
    def __init__(self):
        self._neurons: Dict[UUID, ShadowNeuron] = {}

    def add(self, n): self._neurons[n.neuron_id] = n
    def get(self, nid): return self._neurons.get(nid)
