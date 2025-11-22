import logging
import asyncio
import math
from uuid import UUID

from genesis import config
from psyche.engine import PsycheEngine
# CORRECTED IMPORTS: Use full package path or ensure relative path works
# Using absolute paths relative to genesis_trinity root is safest here
from neuro_genome.affective import ALL_PRIMAL_AXES
from neuro_genome.drive import ALL_DRIVES

logger = logging.getLogger(__name__)

class EgoEngine:
    """
    The Identity Defense System.
    Maintains the stability of the 'SelfConstruct' by rejecting dissonant
    thoughts, while accepting innate biological drives.
    """
    def __init__(self, psyche: PsycheEngine):
        self.psyche = psyche
        self.self_freq = 100.0
        self.strength = 0.8
        self.construct = [] # List of UUIDs considered "Me"
        
        # Build the whitelist of Innate Frequencies (Biology is Self)
        self.innate_frequencies = set()
        for axis in ALL_PRIMAL_AXES:
            self.innate_frequencies.add(axis.base_frequency)
        for drive in ALL_DRIVES:
            self.innate_frequencies.add(drive.base_frequency)
            
        logger.info(f"EgoEngine initialized. Biology whitelisted ({len(self.innate_frequencies)} frequencies).")

    async def monitor(self):
        while self.psyche.is_running:
            await self._broadcast_self()
            await self._defend()
            await asyncio.sleep(config.TICK_DURATION)

    async def _broadcast_self(self):
        # The "I AM" signal - reinforces the core identity frequency
        self.psyche.inject_wave(self.self_freq, 0.2 * self.strength, 0)

    async def _defend(self):
        """
        Scans for alien waves.
        If a wave is high-amplitude, foreign frequency, AND NOT BIOLOGICAL, reject it.
        """
        for nid, wave in list(self.psyche.active_waves.items()):
            if nid in self.construct: continue
            
            # Check if this is an Innate Biological Signal
            is_innate = any(math.isclose(wave.frequency, f, abs_tol=0.01) for f in self.innate_frequencies)
            if is_innate:
                continue # Allow biology to pass through the Ego

            # Dissonance Check
            if abs(wave.frequency - self.self_freq) > 10.0 and wave.initial_amplitude > 0.5:
                logger.warning(f"EGO DEFENSE: Rejecting alien thought (Freq: {wave.frequency:.2f}).")
                
                # Destructive Interference (The Block)
                wave.phase_shift += math.pi 
                wave.initial_amplitude *= (1.0 - self.strength)
