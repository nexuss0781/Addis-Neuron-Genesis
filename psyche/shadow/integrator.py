import asyncio
import logging
from genesis_trinity.psyche.hypothalamus import ConsciousEvent
from .dark_web import DarkWeb
from .scavenger import TraumaScavenger
from .doppelganger import Doppelganger

logger = logging.getLogger(__name__)

class ShadowIntegrator:
    """The Warden."""
    def __init__(self, psyche, hypo, metabolic):
        self.psyche = psyche
        self.hypo = hypo
        self.metabolic = metabolic
        self.dark_web = DarkWeb()
        self.scavenger = TraumaScavenger(self.dark_web)
        self.doppel = Doppelganger(self.dark_web)
        logger.info("ShadowIntegrator initialized.")

    async def monitor(self):
        while self.psyche.is_running:
            self.doppel.grow()
            if self.doppel.hijack():
                logger.critical("SHADOW EVENT: HIJACK!")
                self.hypo.report_event("THREAT") # Force Panic
                self.doppel.power = 0.0
            await asyncio.sleep(1.0)

    def repress(self, nid, intensity):
        n = self.metabolic.graph.get_neuron(nid)
        name = n.payload.get('name', 'Unknown') if n else 'Unknown'
        logger.critical(f"REPRESSION: Casting '{name}' into Abyss.")
        
        self.scavenger.feed(name)
        
        # Dampen twin
        twin = self.psyche.r_graph.get_neuron(nid)
        if twin:
            for c in twin.connections: c.weight *= (1.0 - intensity)
