import logging
import asyncio
import math
from genesis_trinity import config

logger = logging.getLogger(__name__)

class EgoEngine:
    """The Identity Defense System."""
    def __init__(self, psyche):
        self.psyche = psyche
        self.self_freq = 100.0
        self.strength = 0.8
        self.construct = []

    async def monitor(self):
        while self.psyche.is_running:
            await self._broadcast_self()
            await self._defend()
            await asyncio.sleep(config.TICK_DURATION)

    async def _broadcast_self(self):
        # The "I AM" signal
        self.psyche.inject_wave(self.self_freq, 0.2 * self.strength, 0)

    async def _defend(self):
        for nid, wave in list(self.psyche.active_waves.items()):
            if nid in self.construct: continue
            
            # Dissonance Check
            if abs(wave.frequency - self.self_freq) > 10.0 and wave.initial_amplitude > 0.5:
                logger.warning("EGO DEFENSE: Rejecting alien thought.")
                # Destructive Interference
                wave.phase_shift += math.pi 
                wave.initial_amplitude *= (1.0 - self.strength)
