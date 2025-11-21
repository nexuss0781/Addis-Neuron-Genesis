import logging
import asyncio
from genesis_trinity import config
from .canvas import OneiricCanvas
from .weaver import NarrativeWeaver
from .crucible import SynthesisCrucible

logger = logging.getLogger(__name__)

class DreamEngine:
    def __init__(self, metabolic):
        self.metabolic = metabolic
        self.is_dreaming = False
        logger.info("DreamEngine initialized.")

    async def dream_cycle(self):
        if self.is_dreaming: return
        self.is_dreaming = True
        logger.warning("--- [DREAM CYCLE INITIATED] ---")

        residue = [nid for _, nid in self.metabolic.firing_trace if self.metabolic.graph.get_neuron(nid)]
        
        canvas = OneiricCanvas()
        canvas.project_residue(self.metabolic.graph, residue)
        weaver = NarrativeWeaver(canvas)
        crucible = SynthesisCrucible(canvas)

        for _ in range(3):
            await weaver.step()
            new_concept = crucible.fuse()
            if new_concept:
                self.metabolic.graph.add_neuron(new_concept)
            await asyncio.sleep(0.5)

        logger.warning("--- [DREAM CYCLE COMPLETE] ---")
        self.is_dreaming = False
