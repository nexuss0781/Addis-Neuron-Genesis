import logging
from typing import List
from neuro_cytoplasm.graph import NeuralGraph
from neuro_genome.schemas import Neuron

logger = logging.getLogger(__name__)

class ValuationCortex:
    """
    The Orbitofrontal Cortex.
    Maintains the 'Value Map' of the brain.
    """
    def __init__(self, graph: NeuralGraph):
        self.graph = graph
        logger.info("ValuationCortex initialized.")

    def predict(self, neurons: List[Neuron]) -> float:
        """Calculates net Expected Value (V) of a thought."""
        total, count = 0.0, 0
        for n in neurons:
            if n.value_confidence > 0.1:
                total += n.expected_value
                count += 1
        return total / count if count else 0.0

    def update(self, nid, reward: float):
        """Updates V using Rescorla-Wagner rule."""
        n = self.graph.get_neuron(nid)
        if not n: return
        
        ALPHA = 0.1 # Learning Rate
        error = reward - n.expected_value
        n.expected_value += ALPHA * error
        n.value_confidence = min(1.0, n.value_confidence + 0.05)
