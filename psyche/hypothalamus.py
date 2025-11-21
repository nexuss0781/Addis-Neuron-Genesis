import asyncio
import logging
from typing import Tuple

from genesis_trinity.neuro_genome.affective import VALENCE_AXIS, AROUSAL_AXIS, DOMINANCE_AXIS
from .engine import PsycheEngine

logger = logging.getLogger(__name__)

class HypothalamusEngine:
    """
    The primal transducer.
    Converts Event -> Energy.
    """
    def __init__(self, psyche: PsycheEngine, metabolic_engine: 'MetabolicEngine'):
        self.psyche = psyche
        self.metabolic = metabolic_engine
        
        # The Genetic Map: Hardcoded physiological responses
        self._event_map = {
            "SUCCESS": (VALENCE_AXIS, 1.0),   # Reward
            "FAILURE": (VALENCE_AXIS, -1.0),  # Punishment
            "PAIN":    (VALENCE_AXIS, -2.0),  # Severe Punishment
            "THREAT":  (AROUSAL_AXIS, 1.0),   # Fight/Flight
            "NOVELTY": (AROUSAL_AXIS, 0.5),   # Interest
            "BOREDOM": (AROUSAL_AXIS, -0.5),  # Low energy
            "CONTROL": (DOMINANCE_AXIS, 1.0), # Empowerment
            "SUBMIT":  (DOMINANCE_AXIS, -1.0) # Submission
        }
        
        # Event Queue (String-based for Phase 2.0 simplicity)
        self.queue: asyncio.Queue[str] = asyncio.Queue()
        
        logger.info("HypothalamusEngine initialized.")

    async def monitor(self):
        """Main loop."""
        while self.psyche.is_running:
            try:
                event_name = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                self._transduce(event_name)
                self.queue.task_done()
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break

    def report_event(self, event_name: str):
        """Public API."""
        try:
            self.queue.put_nowait(event_name)
        except asyncio.QueueFull:
            pass

    def _transduce(self, event_name: str):
        """
        Injects the corresponding wave into the Psyche.
        """
        if event_name not in self._event_map:
            return

        axis, polarity = self._event_map[event_name]
        logger.debug(f"HYPOTHALAMUS: Transducing {event_name} -> {axis.name} ({polarity})")
        
        self.psyche.inject_wave(
            frequency=axis.base_frequency,
            amplitude=polarity * 2.0, # High intensity for events
            tick=self.metabolic.current_tick
        )
