import logging
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List

logger = logging.getLogger(__name__)

class OrganType(Enum):
    """The functional systems of the bio-digital body."""
    BATTERY = auto()      # Cognitive Energy (The Fuel)
    INTEGRITY = auto()    # Neural Coherence (The Structure)
    PLASTICITY = auto()   # Learning Capability (The Growth)
    DAMPENERS = auto()    # Signal-to-Noise Control (The Sanity)

@dataclass
class Organ:
    """
    A single physiological system.
    """
    type: OrganType
    current_value: float = 1.0
    max_value: float = 1.0
    
    # Intrinsic Properties
    decay_rate: float = 0.001       # Entropy: Natural loss over time
    recovery_rate: float = 0.005    # Healing: Gain during sleep
    
    # Dynamic State
    temperature: float = 0.0        # Stress level (0.0 - 1.0)
    is_infected: bool = False       # Pathogen presence

@dataclass
class Dependency:
    """
    A physical link defining how one organ affects another.
    """
    source: OrganType
    target: OrganType
    weight: float 
    description: str

class SomaticGraph:
    """
    The Master Anatomy. 
    Contains the organs and hardwires the laws of their interaction.
    """
    def __init__(self):
        self.organs: Dict[OrganType, Organ] = {}
        self.dependencies: List[Dependency] = []
        self._init_morphology()
        logger.info("SomaticGraph initialized: Anatomy constructed.")

    def _init_morphology(self):
        # 1. Instantiate Organs with specific metabolic profiles
        self.organs[OrganType.BATTERY] = Organ(OrganType.BATTERY, decay_rate=0.002)
        self.organs[OrganType.INTEGRITY] = Organ(OrganType.INTEGRITY, decay_rate=0.0005)
        self.organs[OrganType.PLASTICITY] = Organ(OrganType.PLASTICITY, decay_rate=0.0) # Only decays via inhibition
        self.organs[OrganType.DAMPENERS] = Organ(OrganType.DAMPENERS, decay_rate=0.001)

        # 2. Hardwire the Physiology
        self.dependencies = [
            # --- The Energy Cascade ---
            # Energy is required for learning. If Battery drops, Plasticity is inhibited.
            Dependency(OrganType.BATTERY, OrganType.PLASTICITY, 0.8, "Energy powers Learning"),
            # Energy maintains sanity filters. Low energy = hallucinations.
            Dependency(OrganType.BATTERY, OrganType.DAMPENERS, 0.5, "Energy powers Dampeners"),

            # --- The Structural Foundation ---
            # If Integrity fails, everything fails.
            Dependency(OrganType.INTEGRITY, OrganType.BATTERY, 0.2, "Structural Efficiency"),
            Dependency(OrganType.INTEGRITY, OrganType.DAMPENERS, 1.0, "Structural Integrity prevents noise"),

            # --- The Metabolic Cost (Negative Feedback loops) ---
            # Learning burns energy rapidly.
            Dependency(OrganType.PLASTICITY, OrganType.BATTERY, -0.3, "Neuroplasticity consumes Energy"),
            # Suppressing noise burns energy.
            Dependency(OrganType.DAMPENERS, OrganType.BATTERY, -0.1, "Dampening consumes Energy"),
        ]

    def get_organ(self, organ_type: OrganType) -> Organ:
        return self.organs[organ_type]
