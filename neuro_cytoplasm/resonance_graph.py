import logging
from uuid import UUID
from typing import Dict
from neuro_genome.schemas import ResonanceNeuron

logger = logging.getLogger(__name__)

class ResonanceGraph:
    """
    The Master Container for the Subconscious Mind (System 1).
    Optimized for wave propagation physics.
    """
    def __init__(self):
        self._neurons: Dict[UUID, ResonanceNeuron] = {}
        logger.info("ResonanceGraph initialized.")

    def add_neuron(self, neuron: ResonanceNeuron):
        self._neurons[neuron.neuron_id] = neuron

    def get_neuron(self, neuron_id: UUID) -> ResonanceNeuron | None:
        return self._neurons.get(neuron_id)

    def __len__(self):
        return len(self._neurons)
