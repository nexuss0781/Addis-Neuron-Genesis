import logging
from .graph import SomaticGraph, OrganType

logger = logging.getLogger(__name__)

class FluxEngine:
    """
    The Physiology Engine.
    Calculates the dynamic flow of resources, entropy, and stress through the
    Somatic Graph on every tick of the universe.
    """
    def __init__(self, graph: SomaticGraph):
        self.graph = graph
        self.is_sleeping = False
        logger.info("FluxEngine initialized: Metabolism active.")

    def update_metabolism(self, cognitive_load: float):
        """
        The heartbeat of the body.
        cognitive_load: 0.0 (Coma) to 1.0 (Maximum Mental Effort).
        """
        # 1. The Cost of Being Alive (Basal Metabolic Rate + Active Load)
        battery = self.graph.get_organ(OrganType.BATTERY)
        base_cost = battery.decay_rate
        active_cost = cognitive_load * 0.01 # Thinking burns fuel
        battery.current_value -= (base_cost + active_cost)

        # 2. Inter-Organ Flux (The Dependency Cascade)
        self._process_dependencies()

        # 3. Thermodynamics (Stress & Heat)
        self._update_thermodynamics(cognitive_load)

        # 4. Recovery (Sleep Cycle)
        if self.is_sleeping:
            self._process_recovery()

        # 5. Clamping (Physical Limits)
        for organ in self.graph.organs.values():
            organ.current_value = max(0.0, min(organ.max_value, organ.current_value))
            organ.temperature = max(0.0, min(1.0, organ.temperature))

    def _process_dependencies(self):
        """
        Propagates influence across the dependency graph.
        This is where "low energy" physically causes "stupidity".
        """
        for dep in self.graph.dependencies:
            source = self.graph.get_organ(dep.source)
            target = self.graph.get_organ(dep.target)
            
            if dep.weight > 0:
                # SUPPORT LINK: Low source starves target.
                # If source is failing (< 50%), it drags the target down.
                if source.current_value < 0.5:
                    deficit = 0.5 - source.current_value
                    drag = deficit * dep.weight * 0.05 # Gradual failure cascade
                    target.current_value -= drag
            else:
                # COST LINK: Active source drains target.
                # If source (e.g. Plasticity) is high, it drains the target (Energy).
                cost = source.current_value * abs(dep.weight) * 0.005
                target.current_value -= cost

    def _update_thermodynamics(self, load: float):
        """
        Manages system temperature (Stress).
        High load generates heat. High heat damages integrity.
        """
        battery = self.graph.get_organ(OrganType.BATTERY)
        integrity = self.graph.get_organ(OrganType.INTEGRITY)

        # Heat Generation
        if load > 0.7:
            # Intense thought generates heat rapidly
            battery.temperature += 0.02
        else:
            # Cooling down
            battery.temperature -= 0.01

        # Thermal Damage (Burnout)
        if battery.temperature > 0.8:
            # Critical Overheat: Physically damaging the brain structure
            damage = (battery.temperature - 0.8) * 0.01
            integrity.current_value -= damage
            # Feedback loop: Damage increases temp further (inflammation)
            integrity.temperature += 0.01 

    def _process_recovery(self):
        """Sleep logic."""
        for organ in self.graph.organs.values():
            # Cooling
            organ.temperature -= 0.05
            # Healing
            organ.current_value += organ.recovery_rate
