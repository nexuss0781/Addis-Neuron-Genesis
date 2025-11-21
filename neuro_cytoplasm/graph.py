import logging
from uuid import UUID, uuid4
from typing import Dict, Set, List, Optional
from neuro_genome.schemas import Neuron
from neuro_genome.enums import NeuronType

logger = logging.getLogger(__name__)

class NeuralGraph:
    """
    The Master Container for the Conscious Mind (System 2).
    Optimized for O(1) lookup and Type-based querying.
    """
    def __init__(self):
        self._neurons: Dict[UUID, Neuron] = {}
        
        # Indexing Reticulum
        self._type_index: Dict[NeuronType, Set[UUID]] = {nt: set() for nt in NeuronType}
        self._name_index: Dict[str, UUID] = {}
        
        logger.info("NeuralGraph initialized.")

    def add_neuron(self, neuron: Neuron):
        """Adds a neuron and updates all indexes."""
        if neuron.neuron_id in self._neurons:
            return # Idempotent

        self._neurons[neuron.neuron_id] = neuron
        self._type_index[neuron.neuron_type].add(neuron.neuron_id)

        if 'name' in neuron.payload:
            name = neuron.payload['name']
            if isinstance(name, str):
                self._name_index[name.lower()] = neuron.neuron_id

    def get_neuron(self, neuron_id: UUID) -> Optional[Neuron]:
        return self._neurons.get(neuron_id)

    def get_neuron_by_name(self, name: str) -> Optional[Neuron]:
        return self.get_neuron(self._name_index.get(name.lower()))

    def get_neurons_by_type(self, neuron_type: NeuronType) -> List[Neuron]:
        ids = self._type_index.get(neuron_type, set())
        return [self._neurons[nid] for nid in ids if nid in self._neurons]
    
    def __len__(self):
        return len(self._neurons)
