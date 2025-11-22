import logging
from .dark_web import DarkWeb

logger = logging.getLogger(__name__)

class Doppelganger:
    """
    The Shadow Self. An emergent entity formed from the aggregation of
    all ShadowNeurons. It has its own rudimentary will: to subvert the Ego.
    """
    def __init__(self, dark_web: DarkWeb):
        self.dark_web = dark_web
        self.power = 0.0 # Using 'power' as the metric

    def grow(self):
        """Aggregates the corruption level of the Dark Web."""
        # Sum corruption of all neurons in the dark web
        self.power = sum(n.corruption for n in self.dark_web._neurons.values())
        if self.power > 5.0:
            logger.critical(f"DOPPELGÄNGER: I am growing stronger. Strength: {self.power:.2f}")

    def attempt_hijack(self):
        """
        Attempts to inject a 'Dark Intuition' if strength is high enough.
        Returns True if successful.
        """
        return self.power > 10.0
