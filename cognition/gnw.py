import logging
import asyncio
from typing import List, Optional
from uuid import UUID

from genesis_trinity import config
from neuro_cytoplasm.graph import NeuralGraph
from neuro_genome.schemas import Neuron
from neuro_genome.enums import NeuronType

logger = logging.getLogger(__name__)

class GlobalNeuronalWorkspace:
    """
    The Stage of Consciousness.
    Selects the most salient neuron cluster and broadcasts it to the entire brain.
    """
    def __init__(self, graph: NeuralGraph):
        self.graph = graph
        self.current_focus: Optional[UUID] = None
        logger.info("GlobalNeuronalWorkspace initialized.")

    def update(self, active_neurons: List[Neuron]):
        """
        Called every tick. Performs the competition for attention.
        """
        if not active_neurons: return

        # 1. Calculate Salience for each candidate
        # Salience = Energy (NAP) + Novelty (Inverse Activation Count) + Value
        best_neuron = None
        max_salience = -1.0

        for neuron in active_neurons:
            # Only high-level neurons enter the workspace
            if neuron.neuron_type not in [NeuronType.LOGICAL_CONCEPT, NeuronType.COGNITIVE_GEDANKE]:
                continue

            # Basic Salience Formula
            salience = neuron.nap
            
            # Value Bias (Dopaminergic influence)
            salience += neuron.expected_value
            
            if salience > max_salience:
                max_salience = salience
                best_neuron = neuron

        # 2. Gating and Ignition
        if best_neuron and max_salience > 0.8:
            if self.current_focus != best_neuron.neuron_id:
                self._ignite_and_broadcast(best_neuron)

    def _ignite_and_broadcast(self, neuron: Neuron):
        """
        The neuron enters the workspace and screams its message to the whole brain.
        """
        self.current_focus = neuron.neuron_id
        neuron.activation_count += 1
        logger.info(f"CONSCIOUS FOCUS: {neuron.payload.get('name', neuron.neuron_id)} (Salience: {neuron.nap:.2f})")
        
        # Broadcast: Boost all connected neighbors
        # This recruits related concepts into the next moment of thought
        for cleft in neuron.connections:
            target = self.graph.get_neuron(cleft.target_id)
            if target:
                target.nap += 0.2 # Top-down attentional boost
