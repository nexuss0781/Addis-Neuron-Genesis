import asyncio
import logging
import math
from dataclasses import dataclass
from typing import Dict, Optional
from uuid import UUID

from genesis import config
from neuro_cytoplasm.graph import NeuralGraph
from neuro_cytoplasm.resonance_graph import ResonanceGraph

logger = logging.getLogger(__name__)

@dataclass
class Wave:
    """
    A sinusoidal wave of energy propagating through the subconscious.
    """
    frequency: float
    initial_amplitude: float
    origin_tick: int
    phase_shift: float = 0.0

    def get_amplitude(self, current_tick: int) -> float:
        """Calculates decayed amplitude."""
        age = current_tick - self.origin_tick
        if age < 0: return 0.0
        # Natural exponential decay of the signal strength
        return self.initial_amplitude * math.exp(-0.1 * age)

    def get_value(self, current_tick: int) -> float:
        """Calculates the instantaneous value of the wave (sinusoid)."""
        amp = self.get_amplitude(current_tick)
        if amp < 0.01: return 0.0
        
        # A * sin(wt + phi)
        return amp * math.sin(
            self.frequency * (current_tick - self.origin_tick) + self.phase_shift
        )

class PsycheEngine:
    """
    The physics engine of the Subconscious Mind (System 1).
    It simulates a continuous field of interfering waves.
    """
    def __init__(self, r_graph: ResonanceGraph, c_graph: NeuralGraph):
        self.r_graph = r_graph
        self.c_graph = c_graph
        self.is_running = False
        
        # State: The sum of all waves at each node (The "Field")
        self.field_values: Dict[UUID, float] = {}
        
        # State: The active waves propagating FROM each node
        self.active_waves: Dict[UUID, Wave] = {}
        
        # Reference to the clock (set during LifeEngine init)
        self.metabolic_engine = None
        
        logger.info("PsycheEngine (Wave Physics) initialized.")

    async def monitor(self):
        """The main simulation loop."""
        if self.is_running: return
        self.is_running = True
        
        while self.is_running:
            if self.metabolic_engine:
                self._update_physics(self.metabolic_engine.current_tick)
            await asyncio.sleep(config.TICK_DURATION)

    def stop(self):
        self.is_running = False

    def inject_wave(self, frequency: float, amplitude: float, tick: int):
        """
        Injects energy into the system. Used by Hypothalamus and DriveMonitor.
        Finds the canonical neuron for the frequency and pulses it.
        """
        for neuron in self.r_graph._neurons.values():
            if math.isclose(neuron.resonance_frequency, frequency, rel_tol=1e-5):
                self.receive_ping(neuron.neuron_id, tick, amplitude)
                return

    def receive_ping(self, neuron_id: UUID, tick: int, amplitude: float = 1.0):
        """
        Triggered by the Conscious Mind (downward flow) or Internal Systems.
        Creates a new wave originating from a specific node.
        """
        neuron = self.r_graph.get_neuron(neuron_id)
        if not neuron: return
        
        # Overwrite previous wave from this node (simplified physics)
        # Phase shift ensures constructive interference for positive amplitude
        phase = 0.0 if amplitude >= 0 else math.pi
        
        self.active_waves[neuron_id] = Wave(
            frequency=neuron.resonance_frequency,
            initial_amplitude=abs(amplitude),
            origin_tick=tick,
            phase_shift=phase
        )

    def _update_physics(self, current_tick: int):
        """
        Calculates the interference pattern for the entire graph.
        """
        next_field = {}
        
        # For every neuron in the subconscious...
        for target_id, target_n in self.r_graph._neurons.items():
            total_interference = 0.0
            
            # Sum the waves from all connected neighbors
            # (In a production graph, we'd iterate incoming edges. 
            # Here we iterate the active waves and check connections for efficiency)
            for source_id, wave in self.active_waves.items():
                # Check if source is connected to target
                # This requires the graph to support reverse lookups or we scan connections.
                # For this implementation phase, we scan the source's connections.
                source_n = self.r_graph.get_neuron(source_id)
                if not source_n: continue
                
                for cleft in source_n.connections:
                    if cleft.target_id == target_id:
                        # Calculate Wave Value at this tick
                        val = wave.get_value(current_tick)
                        # Apply Synaptic Modulation (Weight & Phase)
                        weighted_val = val * cleft.weight
                        total_interference += weighted_val
            
            # Also add the neuron's own active wave (Self-Resonance)
            if target_id in self.active_waves:
                total_interference += self.active_waves[target_id].get_value(current_tick)

            next_field[target_id] = total_interference

        self.field_values = next_field
        
        # Cleanup dead waves
        self.active_waves = {
            nid: w for nid, w in self.active_waves.items() 
            if w.get_amplitude(current_tick) > 0.01
        }
