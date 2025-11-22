import logging
from uuid import UUID
from typing import Dict

from neuro_cytoplasm.graph import NeuralGraph
from neuro_genome.schemas import Neuron, SynapticCleft
from neuro_genome.enums import NeuronType, SynapseType

logger = logging.getLogger(__name__)

class WordEncoder:
    """
    Implements the Predictive Hierarchical Encoding protocol.
    Shared by Gestation and Cognition.
    """
    def __init__(self, graph: NeuralGraph, alphabet_cache: Dict[str, UUID]):
        self.graph = graph
        self.alphabet_cache = alphabet_cache

    def encode_word(self, word_neuron: Neuron):
        """
        Builds the complete, bidirectional, positionally-weighted neural circuit
        for a single word neuron.
        """
        word_str = word_neuron.payload.get('name')
        if not word_str: return

        previous_char_neuron_id = None
        
        for i, char in enumerate(word_str.lower()):
            char_neuron_id = self.alphabet_cache.get(char)
            if not char_neuron_id: continue

            # 1. Top-Down Priming (Word -> Char)
            word_neuron.connections.append(
                SynapticCleft(char_neuron_id, 1.0, SynapseType.ASSOCIATIVE)
            )

            # 2. Bottom-Up Recognition (Char -> Word)
            char_neuron = self.graph.get_neuron(char_neuron_id)
            if char_neuron:
                w = 1.0 / (1.0 + i) 
                char_neuron.connections.append(
                    SynapticCleft(word_neuron.neuron_id, w, SynapseType.HIERARCHICAL)
                )

            # 3. Positional Chain (Char -> Char)
            if previous_char_neuron_id:
                prev_char_neuron = self.graph.get_neuron(previous_char_neuron_id)
                if prev_char_neuron:
                    prev_char_neuron.connections.append(
                        SynapticCleft(char_neuron_id, 1.0, SynapseType.ASSOCIATIVE)
                    )
            
            previous_char_neuron_id = char_neuron_id
