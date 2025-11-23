import logging
import random
from typing import List
from neuro_cytoplasm.graph import NeuralGraph
from neuro_genome.enums import NeuronType

logger = logging.getLogger(__name__)

class LexicalSelector:
    """
    Chooses the best word for a concept based on Tone.
    """
    def __init__(self, graph: NeuralGraph):
        self.graph = graph

    def select_word(self, concept_id, tone="NEUTRAL"):
        """
        Returns the best LINGUISTIC_WORD UUID for a CONCEPT UUID.
        """
        concept = self.graph.get_neuron(concept_id)
        if not concept: return None

        candidates = []
        for c in concept.connections:
            target = self.graph.get_neuron(c.target_id)
            if target and target.neuron_type == NeuronType.LINGUISTIC_WORD:
                candidates.append(target)
        
        if not candidates: return None

        # In a full system, we'd check the word's emotional charge vs tone.
        # For now, we pick the strongest link.
        # (Simplified)
        return candidates[0].neuron_id
