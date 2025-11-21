.mimport logging
logger = logging.getLogger(__name__)

class Doppelganger:
    """The Anti-Self."""
    def __init__(self, dark_web):
        self.web = dark_web
        self.power = 0.0

    def grow(self):
        self.power = sum(n.corruption for n in self.web._neurons.values())
        if self.power > 5.0:
            logger.critical(f"DOPPELGÄNGER: Strength {self.power:.2f}")

    def hijack(self):
        return self.power > 10.0
