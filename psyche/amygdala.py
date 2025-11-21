import asyncio
import hashlib
import logging
import math
from typing import Tuple, Optional

from genesis_trinity import config
from neuro_genome.schemas import ResonanceNeuron, ResonanceCleft
from neuro_genome.enums import NeuronType
from genesis_trinity.neuro_genome.affective import ALL_PRIMAL_AXES
from .engine import PsycheEngine, ResonanceGraph

logger = logging.getLogger(__name__)

class AmygdalaEngine:
    """
    The Emotion Factory.
    Detects stable affective patterns and crystallizes them into emotions.
    """
    def __init__(self, psyche: PsycheEngine, graph: ResonanceGraph, metabolic: 'MetabolicEngine'):
        self.psyche = psyche
        self.r_graph = graph
        self.metabolic = metabolic
        
        self._current_pattern = None
        self._stability_counter = 0
        self._axis_freqs = {a.base_frequency for a in ALL_PRIMAL_AXES}

        logger.info("AmygdalaEngine initialized.")

    async def monitor(self):
        while self.psyche.is_running:
            await self._detect_and_crystallize()
            await asyncio.sleep(config.TICK_DURATION * 5)

    def _scan_field(self) -> Optional[Tuple]:
        """Generates a signature of the current emotional field."""
        active_axes = []
        total_energy = 0.0
        
        # Check the canonical axis neurons
        for nid, val in self.psyche.field_values.items():
            neuron = self.r_graph.get_neuron(nid)
            if not neuron: continue
            
            if neuron.resonance_frequency in self._axis_freqs:
                amp = abs(val)
                total_energy += amp
                if amp > 0.5:
                    # Quantize to create stable buckets
                    q_val = int(val * 5) 
                    active_axes.append((neuron.resonance_frequency, q_val))
        
        if total_energy < 2.0 or len(active_axes) < 2:
            return None
            
        active_axes.sort()
        return tuple(active_axes)

    async def _detect_and_crystallize(self):
        pattern = self._scan_field()
        
        # Stability Check
        if pattern and pattern == self._current_pattern:
            self._stability_counter += 1
        else:
            self._current_pattern = pattern
            self._stability_counter = 0
            return

        if self._stability_counter >= 5:
            # Context Check (Is the mind active?)
            if not self._is_mind_active():
                self._stability_counter = 0
                return

            # Crystallize
            self._birth_emotion(pattern)
            self._stability_counter = 0

    def _is_mind_active(self):
        """Checks if any significant concept fired recently."""
        # Look back 10 ticks
        trace = list(self.metabolic.firing_trace)[-10:]
        for _, nid in trace:
            n = self.metabolic.graph.get_neuron(nid)
            if n and n.neuron_type == NeuronType.LOGICAL_CONCEPT:
                return True
        return False

    def _birth_emotion(self, pattern):
        """Creates the new Emotion Neuron."""
        # Deterministic ID based on the pattern recipe
        sig = str(pattern).encode()
        freq = (int(hashlib.sha256(sig).hexdigest(), 16) % 5000) / 100.0
        
        # Check existence
        for n in self.r_graph._neurons.values():
            if math.isclose(n.resonance_frequency, freq):
                return # Already exists

        logger.warning(f"AMYGDALA: Crystallizing new Emotion (Freq: {freq}) from pattern {pattern}")
        
        # Create Node
        emotion = ResonanceNeuron(resonance_frequency=freq)
        # Manually override type for clarity in debugs, though init=False usually handles it
        emotion.neuron_type = NeuronType.EMOTIONAL_PROTOTYPE 
        self.r_graph.add_neuron(emotion)

        # Wire it to the Axes (The Recipe)
        for axis_freq, _ in pattern:
            # Find axis neuron
            axis_n = next(n for n in self.r_graph._neurons.values() if math.isclose(n.resonance_frequency, axis_freq))
            # Link: Emotion -> Axis
            emotion.connections.append(ResonanceCleft(axis_n.neuron_id, 1.0, 0.0))
