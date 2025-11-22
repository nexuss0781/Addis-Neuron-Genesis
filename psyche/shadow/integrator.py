import asyncio
import logging
from uuid import UUID

# CORRECTED: Removed ConsciousEvent import
from psyche.hypothalamus import HypothalamusEngine
from neuro_mitochondria.engine import MetabolicEngine
from .dark_web import DarkWeb
from .scavenger import TraumaScavenger
from .doppelganger import Doppelganger

logger = logging.getLogger(__name__)

class ShadowIntegrator:
    """
    The Warden of the Abyss. Manages the Dark Web, the Scavenger, and the Doppelgänger.
    """
    def __init__(self, psyche_engine, hypothalamus: HypothalamusEngine, metabolic_engine: MetabolicEngine):
        self.psyche = psyche_engine
        self.hypothalamus = hypothalamus
        self.metabolic = metabolic_engine
        
        # The Abyssal Architecture
        self.dark_web = DarkWeb()
        self.scavenger = TraumaScavenger(self.dark_web)
        self.doppelganger = Doppelganger(self.dark_web)
        
        logger.info("ShadowIntegrator (Abyssal Architecture) initialized.")

    async def monitor(self):
        while self.psyche.is_running:
            self.doppelganger.grow()
            
            if self.doppelganger.attempt_hijack():
                logger.critical("SHADOW EVENT: The Doppelgänger has hijacked the Intuition Conduit!")
                # CORRECTED: Pass simple string event
                self.hypothalamus.report_event("THREAT") 
                # Reset strength (Catharsis)
                self.doppelganger.power = 0.0 # Corrected attribute name from strength to power based on Doppelganger class
                
            await asyncio.sleep(1.0)

    def repress(self, neuron_id: UUID, intensity: float):
        """
        The core logic for repressing a memory. Now feeds the Dark Web.
        """
        neuron = self.metabolic.graph.get_neuron(neuron_id)
        name = neuron.payload.get('name', 'Unknown') if neuron else 'Unknown'
        
        logger.critical(f"REPRESSION: Casting '{name}' into the Abyss.")
        
        # 1. Scavenge the concept
        self.scavenger.feed(name)
        
        # 2. Dampen the conscious link (Standard repression)
        subconscious_twin = self.psyche.r_graph.get_neuron(neuron_id)
        if subconscious_twin:
            for cleft in subconscious_twin.connections:
                cleft.weight *= (1.0 - intensity)
