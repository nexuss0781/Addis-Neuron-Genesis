import logging
from uuid import UUID
from typing import Dict, List

from neuro_cytoplasm.graph import NeuralGraph
from neuro_genome.schemas import Neuron, SynapticCleft

logger = logging.getLogger(__name__)

class OneiricCanvas:
    """The Dream Sandbox."""
    def __init__(self):
        self.sandbox: Dict[UUID, Neuron] = {}
        logger.info("OneiricCanvas initialized.")

    def project_residue(self, graph: NeuralGraph, active_ids: List[UUID]):
        for nid in active_ids:
            orig = graph.get_neuron(nid)
            if orig:
                # Clone
                clone = Neuron(
                    neuron_id=orig.neuron_id, 
                    neuron_type=orig.neuron_type, 
                    payload=orig.payload.copy(), 
                    nap=0.5
                )
                # Weak Connections for Plasticity
                clone.connections = [SynapticCleft(c.target_id, c.weight * 0.8, c.type) for c in orig.connections]
                self.sandbox[nid] = clone

    def get(self, nid): return self.sandbox.get(nid)
    def add(self, n): self.sandbox[n.neuron_id] = n
