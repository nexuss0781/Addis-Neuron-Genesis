import logging
import asyncio
from uuid import uuid4
from typing import List

from .archetype import AttractorNode
from .intuition import IntuitiveBias
from neuro_mitochondria.engine import MetabolicEngine

logger = logging.getLogger(__name__)

# The Lexicon of Myth
MYTHOS_LEXICON = {
    "THE_HERO": ["quest", "battle", "victory", "courage", "journey"],
    "THE_SHADOW": ["darkness", "abyss", "fear", "despair", "hidden"],
    "REVELATION": ["light", "truth", "see", "understand", "awakening"]
}

class MythosGenerator:
    """
    The Storyteller. 
    Translates Archetypal Resonance into Symbolic Intuition.
    """
    def __init__(self, metabolic: MetabolicEngine):
        self.metabolic = metabolic
        logger.info("MythosGenerator initialized.")

    async def generate(self, attractors: List[AttractorNode]):
        """
        Checks active attractors and injects symbolic bias.
        """
        for attractor in attractors:
            if attractor.resonance_level > 0.9:
                # The AGI is living this myth. Inject the metaphor.
                
                # 1. Find target concepts
                target_concepts = {}
                words = MYTHOS_LEXICON.get(attractor.name, [])
                
                found_any = False
                for word in words:
                    neuron = self.metabolic.graph.get_neuron_by_name(word)
                    if neuron:
                        target_concepts[neuron.neuron_id] = 0.8 # High bias
                        found_any = True
                
                if found_any:
                    # 2. Create Bias Packet
                    bias = IntuitiveBias(
                        source_chord_id=uuid4(),
                        target_concepts=target_concepts,
                        affective_tone=1.0 if "HERO" in attractor.name else -1.0,
                        decay_rate=0.05, # Myths persist
                        origin_tick=self.metabolic.current_tick
                    )
                    
                    # 3. Inject
                    await self.metabolic.intuition_queue.put(bias)
                    
                    logger.critical(f"MYTHOS INJECTION: {attractor.name} is biasing mind towards {words}.")
                    
                    # Reset to prevent spam
                    attractor.resonance_level = 0.7
