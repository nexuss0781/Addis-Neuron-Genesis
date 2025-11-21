import logging
import random
from neuro_genome.schemas import SynapticCleft
from neuro_genome.enums import SynapseType

logger = logging.getLogger(__name__)

class NarrativeWeaver:
    """The Dream Director."""
    def __init__(self, canvas):
        self.canvas = canvas
        self.act = 0

    async def step(self):
        self.act += 1
        if self.act == 1: self._inciting()
        elif self.act == 2: self._rising()
        elif self.act == 3: self._climax()

    def _inciting(self):
        logger.info("DREAM: Act 1 - The Incident.")
        keys = list(self.canvas.sandbox.keys())
        if keys:
            self.canvas.get(random.choice(keys)).nap = 2.0

    def _rising(self):
        logger.info("DREAM: Act 2 - The Struggle.")
        # Force associations
        active = [n for n in self.canvas.sandbox.values() if n.nap > 0.5]
        for i in range(len(active)-1):
            active[i].connections.append(SynapticCleft(active[i+1].neuron_id, 0.5, SynapseType.ASSOCIATIVE))

    def _climax(self):
        logger.info("DREAM: Act 3 - The Climax.")
