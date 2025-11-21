import logging
from collections import deque
from typing import List

from genesis_trinity import config
from neuro_genome.symbolic import SymbolicVector
from neuro_mitochondria.engine import MetabolicEngine

logger = logging.getLogger(__name__)

class NarrativeArcEngine:
    """
    Tracks the trajectory of the AGI's experience through 5D Meaning Space.
    It calculates the 'Derivative of Experience' to detect plot twists.
    """
    def __init__(self, metabolic_engine: MetabolicEngine):
        self.metabolic = metabolic_engine
        # A rolling buffer of (tick, SymbolicVector)
        self.narrative_trace: deque = deque(maxlen=1000)
        logger.info("NarrativeArcEngine initialized.")

    def update(self):
        """
        Called on every tick. Calculates the 'Center of Gravity' of the current
        conscious mind in Symbolic Space and records it.
        """
        # 1. Identify Active Concepts
        # We look at neurons that fired in the last 5 ticks (Short-Term Memory)
        recent_firings = [
            nid for tick, nid in self.metabolic.firing_trace 
            if self.metabolic.current_tick - tick <= 5
        ]
        
        active_vectors = []
        for nid in recent_firings:
            neuron = self.metabolic.graph.get_neuron(nid)
            if neuron and neuron.symbolic_vector:
                # Convert dict back to object
                vec = SymbolicVector.from_dict(neuron.symbolic_vector)
                active_vectors.append(vec)
        
        if not active_vectors: return

        # 2. Calculate Mean Vector (The Moment)
        # Start with zero vector
        total_vec = SymbolicVector(0,0,0,0,0)
        for v in active_vectors:
            total_vec = SymbolicVector(
                total_vec.creation_destruction + v.creation_destruction,
                total_vec.order_chaos + v.order_chaos,
                total_vec.self_other + v.self_other,
                total_vec.light_dark + v.light_dark,
                total_vec.stasis_change + v.stasis_change
            )
            
        # Simple normalization (average)
        count = len(active_vectors)
        moment = SymbolicVector(
            total_vec.creation_destruction / count,
            total_vec.order_chaos / count,
            total_vec.self_other / count,
            total_vec.light_dark / count,
            total_vec.stasis_change / count
        )
        
        # 3. Record
        self.narrative_trace.append((self.metabolic.current_tick, moment))

    def get_trajectory(self, window: int = 50) -> SymbolicVector:
        """
        Calculates the vector difference between NOW and THEN.
        This represents the 'Plot Direction'.
        """
        if len(self.narrative_trace) < window:
            return SymbolicVector(0,0,0,0,0)
            
        start_moment = self.narrative_trace[-window][1]
        end_moment = self.narrative_trace[-1][1]
        
        return SymbolicVector(
            end_moment.creation_destruction - start_moment.creation_destruction,
            end_moment.order_chaos - start_moment.order_chaos,
            end_moment.self_other - start_moment.self_other,
            end_moment.light_dark - start_moment.light_dark,
            end_moment.stasis_change - start_moment.stasis_change
        )
