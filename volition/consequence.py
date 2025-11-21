import logging
from soma.graph import OrganType

logger = logging.getLogger(__name__)

class ConsequenceSystem:
    """The Enforcer."""
    def __init__(self, soma):
        self.soma = soma

    def punish(self, severity):
        logger.critical(f"CONSEQUENCE: PUNISHMENT ({severity:.2f})")
        bat = self.soma.graph.get_organ(OrganType.BATTERY)
        integ = self.soma.graph.get_organ(OrganType.INTEGRITY)
        
        bat.current_value -= 0.2 * severity
        integ.current_value -= 0.1 * severity

    def heal(self):
        logger.critical("CONSEQUENCE: HEALING")
        ba
