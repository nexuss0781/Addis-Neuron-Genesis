import logging
import random
from uuid import uuid4

from neuro_cytoplasm.graph import NeuralGraph
from neuro_cytoplasm.resonance_graph import ResonanceGraph
from neuro_genome.schemas import ResonanceNeuron, ResonanceCleft

logger = logging.getLogger(__name__)

class TwinForge:
    """
    Creates the Subconscious Mind (ResonanceGraph) as a shadow reflection
    of the Conscious Mind (NeuralGraph).
    """
    def __init__(self, c_graph: NeuralGraph, r_graph: ResonanceGraph):
        self.c_graph = c_graph
        self.r_graph = r_graph

    def forge(self):
        logger.info("Initiating The Great Twinning...")
        
        # 1. Create Twin Neurons
        for c_neuron in self.c_graph._neurons.values():
            # Deterministic Frequency Generation
            # This ensures the same concept always has the same frequency
            # Frequency range 0.1 - 50.0 Hz
            seed_str = c_neuron.payload.get('name', str(c_neuron.neuron_id))
            freq = (hash(seed_str) % 5000) / 100.0 + 0.1
            
            r_neuron = ResonanceNeuron(
                neuron_id=c_neuron.neuron_id, # SHARED ID
                resonance_frequency=freq
            )
            self.r_graph.add_neuron(r_neuron)

        # 2. Mirror Topology (The Shadow Graph)
        # Create weak resonance links where conscious links exist.
        # This allows the subconscious to "flow" along the same paths as the mind.
        links_created = 0
        for c_src in self.c_graph._neurons.values():
            r_src = self.r_graph.get_neuron(c_src.neuron_id)
            
            for c_cleft in c_src.connections:
                r_tgt = self.r_graph.get_neuron(c_cleft.target_id)
                if r_tgt:
                    # Weak weight (0.1) so subconscious is associative, not rigid
                    r_src.connections.append(ResonanceCleft(r_tgt.neuron_id, 0.1, 0.0))
                    links_created += 1
        
        logger.info(f"Twinning complete. {len(self.r_graph)} resonators and {links_created} shadow links created.")
