import logging
import random
from uuid import uuid4
from typing import List, Tuple

from neuro_cytoplasm.graph import NeuralGraph
from neuro_cytoplasm.resonance_graph import ResonanceGraph
from neuro_genome.schemas import ResonanceNeuron, ResonanceCleft

logger = logging.getLogger(__name__)

class TwinForge:
    """
    Creates the Subconscious Mind (ResonanceGraph) as a shadow reflection
    of the Conscious Mind (NeuralGraph).
    Memory-optimized for large-scale neural networks.
    """
    def __init__(self, c_graph: NeuralGraph, r_graph: ResonanceGraph):
        self.c_graph = c_graph
        self.r_graph = r_graph

    def forge(self):
        logger.info("Initiating The Great Twinning...")
        
        # 1. Create Twin Neurons (memory efficient - no duplicate IDs)
        neuron_count = len(self.c_graph._neurons)
        logger.info(f"Forging {neuron_count} resonant twins...")
        
        batch_size = 5000
        batch_count = 0
        
        for i, (c_neuron_id, c_neuron) in enumerate(self.c_graph._neurons.items()):
            # Deterministic Frequency Generation
            seed_str = c_neuron.payload.get('name', str(c_neuron.neuron_id))
            freq = (hash(seed_str) % 5000) / 100.0 + 0.1
            
            r_neuron = ResonanceNeuron(
                neuron_id=c_neuron_id, # SHARED ID - saves memory
                resonance_frequency=freq
            )
            self.r_graph._neurons[c_neuron_id] = r_neuron
            
            if (i + 1) % batch_size == 0:
                batch_count += 1
                logger.info(f"Forged {i + 1}/{neuron_count} resonators...")
        
        logger.info(f"Created {len(self.r_graph)} resonator neurons.")
        
        # 2. Mirror Topology (Sparse Shadow Graph)
        # Only create resonance links for significant conscious connections
        # This reduces memory footprint while preserving essential topology
        logger.info("Creating sparse shadow topology...")
        links_created = 0
        min_weight_threshold = 0.5  # Only mirror significant connections
        
        for i, (c_src_id, c_src) in enumerate(self.c_graph._neurons.items()):
            if i % 10000 == 0 and i > 0:
                logger.info(f"Processed {i}/{neuron_count} neurons for shadow links...")
            
            r_src = self.r_graph._neurons.get(c_src_id)
            if not r_src:
                continue
            
            # Filter connections by weight threshold to reduce memory
            significant_connections = [
                c for c in c_src.connections 
                if abs(c.weight) >= min_weight_threshold
            ]
            
            for c_cleft in significant_connections:
                # Check if target exists in resonance graph
                if c_cleft.target_id in self.r_graph._neurons:
                    # Create weak resonance link
                    r_cleft = ResonanceCleft(
                        target_id=c_cleft.target_id, 
                        weight=0.1 * abs(c_cleft.weight),  # Scaled weight
                        phase_shift=0.0
                    )
                    r_src.connections.append(r_cleft)
                    links_created += 1
        
        logger.info(f"Twinning complete. {len(self.r_graph)} resonators and {links_created} shadow links created.")
        logger.info(f"Memory efficiency: {(links_created / max(1, sum(len(n.connections) for n in self.c_graph._neurons.values()))) * 100:.1f}% of conscious connections mirrored.")
