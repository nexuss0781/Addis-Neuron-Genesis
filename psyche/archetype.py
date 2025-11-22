import asyncio
import logging
from dataclasses import dataclass
from typing import List

from genesis import config
from neuro_genome.symbolic import SymbolicVector
from .narrative_arc import NarrativeArcEngine
from neuro_mitochondria.engine import MetabolicEngine

logger = logging.getLogger(__name__)

@dataclass
class AttractorNode:
    name: str
    position: SymbolicVector # The 5D coordinate of the theme
    radius: float
    resonance_level: float = 0.0

class ArchetypeCortex:
    """
    The Deep Web. 
    Monitors the Narrative Arc for resonance with universal Archetypes.
    """
    def __init__(self, narrative: NarrativeArcEngine, metabolic: MetabolicEngine):
        self.narrative = narrative
        self.metabolic = metabolic # Needed to inject Mythos
        self.attractors: List[AttractorNode] = []
        self.is_running = False
        self._init_archetypes()
        
        # We need the MythosGenerator (circular dep handled via property or direct instantiation later)
        self.mythos_generator = None 
        
        logger.info("ArchetypeCortex initialized.")

    def _init_archetypes(self):
        # 1. THE HERO (Creation + Change + Self)
        self.attractors.append(AttractorNode(
            name="THE_HERO",
            position=SymbolicVector(0.8, 0.0, 0.9, 0.5, -0.8),
            radius=0.5
        ))
        # 2. THE SHADOW (Destruction + Chaos + Dark)
        self.attractors.append(AttractorNode(
            name="THE_SHADOW",
            position=SymbolicVector(-0.8, -0.9, 0.0, -0.9, -0.5),
            radius=0.5
        ))
        # 3. REVELATION (Order + Light + Change)
        self.attractors.append(AttractorNode(
            name="REVELATION",
            position=SymbolicVector(0.5, 0.9, 0.0, 1.0, -0.7),
            radius=0.5
        ))

    async def monitor(self):
        if self.is_running: return
        self.is_running = True
        
        while self.is_running:
            self.narrative.update() # Update trace
            await self._check_resonance()
            
            # If MythosGenerator is attached, run it
            if self.mythos_generator:
                await self.mythos_generator.generate(self.attractors)
                
            await asyncio.sleep(config.TICK_DURATION)

    def stop(self):
        self.is_running = False

    async def _check_resonance(self):
        # Get direction (normalized)
        traj = self.narrative.get_trajectory(window=50)
        # Dot product logic requires vectors to be roughly unit length or normalized
        # For simplicity, we just do a raw dot product of the components
        
        for attractor in self.attractors:
            # Dot Product: Alignment of Trajectory with Archetype
            alignment = (
                traj.creation_destruction * attractor.position.creation_destruction +
                traj.order_chaos * attractor.position.order_chaos +
                traj.self_other * attractor.position.self_other +
                traj.light_dark * attractor.position.light_dark +
                traj.stasis_change * attractor.position.stasis_change
            )
            
            # If alignment is positive and strong, resonance increases
            if alignment > (1.0 - attractor.radius):
                attractor.resonance_level = min(1.0, attractor.resonance_level + 0.05)
                if attractor.resonance_level > 0.9:
                    logger.info(f"ARCHETYPE RESONANCE: {attractor.name} (Level: {attractor.resonance_level:.2f})")
            else:
                # Decay
                attractor.resonance_level = max(0.0, attractor.resonance_level - 0.01)
