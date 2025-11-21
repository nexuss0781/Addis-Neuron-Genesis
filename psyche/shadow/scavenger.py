import logging
from .dark_web import ShadowNeuron

logger = logging.getLogger(__name__)

class TraumaScavenger:
    """The Hunter."""
    def __init__(self, dark_web):
        self.dark_web = dark_web

    def feed(self, name: str):
        logger.critical(f"SHADOW SCAVENGER: Consuming '{name}'.")
        n = ShadowNeuron(resonance_frequency=13.0, corruption=1.0)
        self.dark_web.add(n)
