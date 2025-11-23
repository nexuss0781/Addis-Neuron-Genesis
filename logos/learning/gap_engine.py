import logging
from neuro_genome.schemas import Neuron
from neuro_genome.enums import NeuronType

logger = logging.getLogger(__name__)

class GapEngine:
    """
    Detects Semantic Voids.
    """
    def __init__(self, graph):
        self.graph = graph

    def detect_gap(self, concept_description: str) -> bool:
        """
        Do we have a word for this?
        """
        # Simplified: Check if description exists
        # In full version: Check if concept vector has a close linguistic neighbor
        return self.graph.get_neuron_by_name(concept_description) is None

    def generate_query(self, concept_desc: str) -> str:
        """
        Asks for help.
        """
        logger.warning(f"GAP DETECTED: No word for '{concept_desc}'")
        return f"I do not know the word for '{concept_desc}'. Can you teach me?"

    def learn_neologism(self, word: str, definition: str):
        """
        Creates the new word.
        """
        # This would call the LexicalSeeder logic
        logger.info(f"LEARNING: Defined '{word}' as '{definition}'")
