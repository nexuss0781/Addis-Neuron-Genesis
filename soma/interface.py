import logging
from typing import Dict, Optional
from dataclasses import dataclass

from .graph import SomaticGraph, OrganType
from .flux import FluxEngine
from .immune import ImmuneSystem

logger = logging.getLogger(__name__)

@dataclass
class VitalStatus:
    """A rich snapshot of physiological state."""
    value: float
    trend: str # 'STABLE', 'RECOVERING', 'DROPPING', 'PLUMMETING'
    is_infected: bool
    temperature: float

class SomaticInterface:
    """
    The Nervous System.
    The bridge between the physical body and the cognitive/motivational systems.
    """
    def __init__(self):
        self.graph = SomaticGraph()
        self.flux = FluxEngine(self.graph)
        self.immune = ImmuneSystem(self.graph)
        
        # History buffer for trend calculation
        self._history: Dict[OrganType, float] = {}
        for organ in self.graph.organs.values():
            self._history[organ.type] = organ.current_value
            
        logger.info("SomaticInterface initialized. Nervous system online.")

    def tick(self, cognitive_load: float = 0.0):
        """
        Advances the entire biological simulation by one tick.
        """
        # 1. Run Systems
        self.immune.update()
        self.flux.update_metabolism(cognitive_load)
        
        # 2. Update History (for trends)
        # We smooth the history to avoid jitter
        for o_type, organ in self.graph.organs.items():
            prev = self._history[o_type]
            # Simple exponential moving average
            self._history[o_type] = (prev * 0.9) + (organ.current_value * 0.1)

    def get_vital(self, organ_name: str) -> VitalStatus:
        """
        Queries the state of an organ.
        Returns rich data including Trends.
        """
        try:
            o_type = OrganType[organ_name.upper()]
        except KeyError:
            logger.error(f"Unknown vital: {organ_name}")
            return VitalStatus(0.0, "UNKNOWN", False, 0.0)

        organ = self.graph.get_organ(o_type)
        prev = self._history[o_type]
        delta = organ.current_value - prev
        
        # The Thresholds of Urgency
        if delta < -0.005:
            trend = "PLUMMETING"
        elif delta < -0.0001:
            trend = "DROPPING"
        elif delta > 0.0001:
            trend = "RECOVERING"
        else:
            trend = "STABLE"

        return VitalStatus(
            value=round(organ.current_value, 3),
            trend=trend,
            is_infected=organ.is_infected,
            temperature=round(organ.temperature, 2)
        )

    # --- Control Interface ---
    def sleep(self):
        self.flux.is_sleeping = True
    
    def wake(self):
        self.flux.is_sleeping = False
        
    def infect(self, disease_name: str):
        # Exposed for testing/narrative events
        self.immune.infect(disease_name, OrganType.INTEGRITY)
