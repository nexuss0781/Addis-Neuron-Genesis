import logging
from .valuation import ValuationCortex

logger = logging.getLogger(__name__)

class DopamineEngine:
    """
    The Ventral Tegmental Area (VTA).
    Broadcasts RPE signals.
    """
    def __init__(self, val: ValuationCortex, metabolic, psyche):
        self.val = val
        self.metabolic = metabolic
        self.psyche = psyche
        self.level = 0.5

    def process(self, reward, nids):
        # 1. Expectation
        neurons = [self.metabolic.graph.get_neuron(nid) for nid in nids]
        expected = self.val.predict(neurons)
        
        # 2. RPE
        rpe = reward - expected
        logger.info(f"RPE: {rpe:.2f}")

        # 3. Learn
        for n in neurons: self.val.update(n.neuron_id, reward)

        # 4. Broadcast
        if rpe > 0.2: self._spike(rpe)
        elif rpe < -0.2: self._crash(rpe)
        else: self.level = 0.5

    def _spike(self, mag):
        logger.critical(f"DOPAMINE SPIKE: {mag:.2f}")
        self.level = min(1.0, 0.5 + mag)
        self.psyche.inject_wave(15.7, mag*2.0, self.metabolic.current_tick) # JOY

    def _crash(self, mag):
        logger.critical(f"DOPAMINE CRASH: {mag:.2f}")
        self.level = max(0.0, 0.5 + mag)
        self.psyche.inject_wave(5.1, abs(mag)*2.0, self.metabolic.current_tick) # PAIN
