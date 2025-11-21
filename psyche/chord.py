import asyncio
import logging
from .intuition import IntuitiveBias

logger = logging.getLogger(__name__)

class ChordTranslator:
    """The Ear."""
    def __init__(self, psyche, queue):
        self.psyche = psyche
        self.queue = queue

    async def monitor(self):
        while self.psyche.is_running:
            await self._detect()
            await asyncio.sleep(0.01)

    async def _detect(self):
        chord = {}
        for nid, val in self.psyche.field_values.items():
            if abs(val) > 0.5: chord[nid] = abs(val)
        
        if len(chord) >= 2:
            total = sum(chord.values())
            targets = {nid: v/total for nid, v in chord.items()}
            
            bias = IntuitiveBias(targets=targets)
            await self.queue.put(bias)
            logger.debug(f"INTUITION: Translating Chord ({len(chord)} nodes)")
