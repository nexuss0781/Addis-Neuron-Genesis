import logging
from typing import Dict, List
from dataclasses import dataclass
from .graph import SomaticGraph, OrganType

logger = logging.getLogger(__name__)

@dataclass
class Pathogen:
    """
    An active agent of corruption.
    It is not just a stat debuff; it is a process that grows and feeds.
    """
    name: str
    target: OrganType
    virulence: float   # Growth rate (0.0 - 1.0)
    resistance: float  # Defense against immune system (0.0 - 1.0)
    severity: float = 0.1 # Current infection load

    def metabolyze(self, graph: SomaticGraph):
        """The pathogen feeds on the host."""
        organ = graph.get_organ(self.target)
        
        # 1. Damage (Feeding)
        damage = self.severity * 0.01
        organ.current_value -= damage
        
        # 2. Replication
        # It grows faster if the host organ is weak
        if organ.current_value < 0.5:
            self.severity = min(1.0, self.severity + (self.virulence * 2))
        else:
            self.severity = min(1.0, self.severity + self.virulence)

class ImmuneSystem:
    """
    The Hunter-Killer system.
    Patrols the Soma, identifies Pathogens, and expends Energy to destroy them.
    """
    def __init__(self, graph: SomaticGraph):
        self.graph = graph
        self.active_infections: Dict[str, Pathogen] = {}
        logger.info("ImmuneSystem initialized. Patrol active.")

    def infect(self, name: str, target: OrganType, virulence: float = 0.05):
        """Introduces a new threat."""
        if name not in self.active_infections:
            logger.warning(f"SOMATIC ALERT: Infection '{name}' detected in {target.name}.")
            self.active_infections[name] = Pathogen(name, target, virulence, resistance=0.5)
            self.graph.get_organ(target).is_infected = True

    def update(self):
        """The Combat Loop."""
        if not self.active_infections: return

        battery = self.graph.get_organ(OrganType.BATTERY)
        
        # 1. Calculate Immune Response Strength
        # Based on available energy. Sickness requires energy.
        immune_power = battery.current_value * 0.2 
        
        # 2. Pay the Cost (Fever)
        # Fighting burns energy.
        battery.current_value -= 0.01 * len(self.active_infections)
        # Fighting generates heat.
        battery.temperature += 0.01 * len(self.active_infections)

        cured = []
        for name, bug in self.active_infections.items():
            # The pathogen attacks
            bug.metabolyze(self.graph)
            
            # The body attacks back
            attack = immune_power
            defense = bug.severity * bug.resistance
            
            if attack > defense:
                # Successful hit
                bug.severity -= 0.05
                if bug.severity <= 0:
                    cured.append(name)
            else:
                # The infection is overwhelming the defenses
                logger.warning(f"IMMUNE FAILURE: Losing ground against '{name}'.")

        # Cleanup
        for name in cured:
            logger.info(f"INFECTION CLEARED: '{name}' neutralized.")
            organ = self.graph.get_organ(self.active_infections[name].target)
            organ.is_infected = False
            del self.active_infections[name]
