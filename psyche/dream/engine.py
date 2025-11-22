import logging
import asyncio
from genesis import config
from .canvas import OneiricCanvas
from .weaver import NarrativeWeaver
from .crucible import SynthesisCrucible
# Import type hints if needed, but avoid circular imports at runtime
# from psyche.engine import PsycheEngine
# from neuro_mitochondria.engine import MetabolicEngine

logger = logging.getLogger(__name__)

class DreamEngine:
    def __init__(self, psyche_engine, metabolic_engine):
        self.psyche = psyche_engine
        self.metabolic = metabolic_engine
        self.is_dreaming = False
        logger.info("DreamEngine initialized.")

    async def dream_cycle(self):
        if self.is_dreaming: return
        self.is_dreaming = True
        logger.warning("--- [DREAM CYCLE INITIATED] ---")

        # 1. Get Residue
        residue = [nid for _, nid in self.metabolic.firing_trace if self.metabolic.graph.get_neuron(nid)]
        
        # 2. Project to Canvas
        canvas = OneiricCanvas()
        canvas.project_residue(self.metabolic.graph, residue)
        
        weaver = NarrativeWeaver(canvas)
        crucible = SynthesisCrucible(canvas)

        # 3. Run Simulation
        for _ in range(3):
            await weaver.step()
            new_concept = crucible.fuse()
            if new_concept:
                # Write back to reality
                self.metabolic.graph.add_neuron(new_concept)
                # Optional: Notify psyche of new concept for resonance?
            
            await asyncio.sleep(0.5)

        logger.warning("--- [DREAM CYCLE COMPLETE] ---")
        self.is_dreaming = False
