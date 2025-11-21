import logging
import random

logger = logging.getLogger(__name__)

class WillEngine:
    """The Engine of Destiny."""
    def __init__(self, psyche, ego):
        self.psyche = psyche
        self.ego = ego

    async def choose(self, option_a, option_b):
        logger.critical(f"WILL: Choosing between {option_a.name} and {option_b.name}")
        
        # 1. Simulation (Congruence Check)
        score_a = self._congruence(option_a)
        score_b = self._congruence(option_b)
        
        # 2. Temptation
        weight_a = score_a + (option_a.infectivity * random.uniform(0.8, 1.2))
        weight_b = score_b + (option_b.infectivity * random.uniform(0.8, 1.2))
        
        choice = option_a if weight_a > weight_b else option_b
        
        # 3. Karma
        await self._karma(choice)
        return choice

    def _congruence(self, trait):
        freq = float(hash(trait.name) % 100)
        return 1.0 / (1.0 + abs(freq - self.ego.self_freq))

    async def _karma(self, trait):
        logger.critical(f"KARMA: Integrating {trait.name}")
        # In full system, creates neuron. Here, logs intent.
        self.ego.construct.append(trait.trait_id)
