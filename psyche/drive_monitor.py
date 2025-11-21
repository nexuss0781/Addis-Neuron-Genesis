import asyncio
import logging
from typing import List

from genesis_trinity import config
from genesis_trinity.health.interface import SomaticInterface
from genesis_trinity.neuro_genome.drive import ALL_DRIVES, DriveAxis
from .engine import PsycheEngine

logger = logging.getLogger(__name__)

class DriveMonitor:
    """
    The Interoceptive Bridge.
    It turns physical need into subconscious pressure.
    """
    def __init__(self, soma: SomaticInterface, psyche: PsycheEngine, metabolic: 'MetabolicEngine'):
        self.soma = soma
        self.psyche = psyche
        self.metabolic = metabolic
        logger.info("DriveMonitor initialized.")

    async def monitor(self):
        while self.psyche.is_running:
            self.soma.tick(cognitive_load=0.1) # Advance the body
            await self._process_drives()
            await asyncio.sleep(config.TICK_DURATION)

    async def _process_drives(self):
        for drive in ALL_DRIVES:
            # 1. Get Vital Status
            status = self.soma.get_vital(drive.linked_organ_name)
            
            # 2. Calculate Deficit
            # If value is 1.0 (Full), deficit is 0.0.
            # If value is 0.2 (Empty), deficit is 0.8.
            deficit = max(0.0, 1.0 - status.value)
            
            # Ignore negligible needs
            if deficit < 0.1: continue

            # 3. Calculate Urgency (The Multiplier)
            urgency = drive.urgency_multiplier
            if status.trend == "DROPPING":
                urgency *= 1.5
            elif status.trend == "PLUMMETING":
                urgency *= 3.0 # Panic State

            # 4. Inject the Drive Wave
            # A continuous hum at the drive's frequency
            amplitude = deficit * urgency
            
            self.psyche.inject_wave(
                frequency=drive.base_frequency,
                amplitude=amplitude,
                tick=self.metabolic.current_tick
            )

            if amplitude > 2.0:
                logger.warning(f"DRIVE SURGE: {drive.name} is critical (Amp: {amplitude:.2f})")
