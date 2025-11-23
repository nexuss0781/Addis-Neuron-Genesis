import logging
from neuro_genome.schemas import SynapticCleft
from neuro_genome.enums import SynapseType
from .buffer import DiscourseBuffer

logger = logging.getLogger(__name__)

class AnaphoraResolver:
    """
    Links pronouns ('it', 'he') to antecedents in the buffer.
    """
    def __init__(self, buffer: DiscourseBuffer, graph):
        self.buffer = buffer
        self.graph = graph

    def resolve(self, pronoun_word: str) -> str | None:
        """
        Returns the name of the referenced entity.
        """
        candidates = self.buffer.get_recent_entities()
        if not candidates: return None

        # Simple heuristic: Match by 'gender/type' (not implemented fully here)
        # For now, return the most recent Noun-Concept
        for cid in candidates:
            neuron = self.graph.get_neuron(cid)
            # Check if it's a valid target (not a verb/adj)
            # (Simplified check)
            if neuron and "POS:NOUN" in [str(c.target_id) for c in neuron.connections]:
                logger.info(f"ANAPHORA: '{pronoun_word}' resolved to '{neuron.payload['name']}'")
                return neuron.payload['name']
                
        return None
