import logging
from uuid import UUID
from typing import Optional, Dict

from neuro_cytoplasm.graph import NeuralGraph

logger = logging.getLogger(__name__)

class GlobalNeuronalWorkspace:
    """
    A simple model of the GNW.
    It identifies the neuron with the highest activation potential (NAP)
    as the current 'focus' of consciousness.
    """
    def __init__(self, c_graph: NeuralGraph, threshold: float = 0.5):
        self.c_graph = c_graph
        self.threshold = threshold
        self.current_focus: Optional[UUID] = None
        self.focus_history = [] # To track the stream of consciousness

    def update_focus(self):
        """
        Scan all neurons to find the one with the highest NAP.
        This is a simplification; a real GNW would involve broadcasting
        and competition, but this captures the essence.
        """
        highest_nap = -1.0
        candidate_focus = None

        for neuron_id, neuron in self.c_graph._neurons.items():
            if neuron.nap > highest_nap:
                highest_nap = neuron.nap
                candidate_focus = neuron_id

        logger.debug(f"Highest NAP in GNW update: {highest_nap}")

        if highest_nap > self.threshold:
            if candidate_focus != self.current_focus:
                self.current_focus = candidate_focus
                self.focus_history.append(self.current_focus)
                logger.debug(f"GNW Focus shifted to: {self.c_graph.get_neuron(self.current_focus)}")
        else:
            self.current_focus = None
