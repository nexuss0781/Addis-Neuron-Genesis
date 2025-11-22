import asyncio
import logging
from typing import List

from genesis import config
# CORRECTED: Import from 'soma' package, not 'health'
from soma.interface import SomaticInterface 
from neuro_genome.drive import ALL_DRIVES, DriveAxis
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
            # 1. Get Status
            # Note: Drive definitions use strings for organ names now to decouple
            # We need to ensure SomaticInterface accepts the string name
            status = self.soma.get_vital(drive.linked_organ_name)
            
            # 2. Calculate Deficit
            deficit = max(0.0, 1.0 - status.value)
            
            if deficit < 0.1: continue

            # 3. Calculate Urgency
            urgency = drive.urgency_multiplier
            if status.trend == "DROPPING":
                urgency *= 1.5
            elif status.trend == "PLUMMETING":
                urgency *= 3.0

            # 4. Inject Wave
            amplitude = deficit * urgency
            
            self.psyche.inject_wave(
                frequency=drive.base_frequency,
                amplitude=amplitude,
                tick=self.metabolic.current_tick
            )

            if amplitude > 2.0:
                logger.warning(f"DRIVE SURGE: {drive.name} is critical (Amp: {amplitude:.2f})")
