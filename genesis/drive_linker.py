import logging
from uuid import uuid4

from neuro_cytoplasm.graph import NeuralGraph
from neuro_cytoplasm.resonance_graph import ResonanceGraph
from neuro_genome.schemas import ResonanceNeuron, ResonanceCleft
from neuro_genome.drive import ALL_DRIVES, DRIVE_ENERGY, DRIVE_GROWTH, DRIVE_INTEGRITY

logger = logging.getLogger(__name__)

class MotivationalAssociator:
    """
    Forges the innate "Instincts" of the organism.
    It connects the canonical Drive neurons to the specific Concept neurons
    that represent their satisfaction.
    """
    def __init__(self, conscious_graph: NeuralGraph, subconscious_graph: ResonanceGraph):
        self.c_graph = conscious_graph
        self.r_graph = subconscious_graph
        self._drive_cache = {}
        logger.info("MotivationalAssociator initialized.")

    def forge_instincts(self):
        """
        The main execution method. Creates Drive neurons and links them.
        """
        logger.info("Forging innate motivational instincts...")
        
        # 1. Create the Canonical Drive Neurons in the Subconscious
        for drive in ALL_DRIVES:
            # Check if drive neuron already exists (from inoculation)
            # For robustness, we scan by frequency
            drive_neuron = None
            for n in self.r_graph._neurons.values():
                if n.resonance_frequency == drive.base_frequency:
                    drive_neuron = n
                    break
            
            if not drive_neuron:
                drive_neuron = ResonanceNeuron(
                    neuron_id=uuid4(),
                    resonance_frequency=drive.base_frequency
                )
                self.r_graph.add_neuron(drive_neuron)
            
            self._drive_cache[drive.name] = drive_neuron
            
        # 2. Link Energy Drive -> "Sleep" / "Rest"
        self._link_drive(DRIVE_ENERGY, ["sleep", "rest", "energy"])
        
        # 3. Link Growth Drive -> "Learn" / "Read"
        self._link_drive(DRIVE_GROWTH, ["learn", "read", "growth", "new"])
        
        # 4. Link Integrity Drive -> "Correct" / "Fix"
        self._link_drive(DRIVE_INTEGRITY, ["correct", "fix", "health"])
        
        logger.info("Instincts forged.")

    def _link_drive(self, drive_constant, target_words: list[str]):
        """
        Helper to create a bidirectional resonance link between a Drive neuron
        and a Concept's subconscious twin.
        """
        drive_neuron = self._drive_cache[drive_constant.name]
        
        for word in target_words:
            # Find the conscious neuron
            conscious_neuron = self.c_graph.get_neuron_by_name(word)
            if conscious_neuron:
                # Find its subconscious twin (same ID)
                twin_id = conscious_neuron.neuron_id
                twin_neuron = self.r_graph.get_neuron(twin_id)
                
                if twin_neuron:
                    # Create strong, bidirectional resonance
                    # Drive -> Concept (Motivation)
                    drive_neuron.connections.append(
                        ResonanceCleft(target_id=twin_id, weight=1.0, phase_shift=0.0)
                    )
                    # Concept -> Drive (Reward Anticipation - simplified)
                    twin_neuron.connections.append(
                        ResonanceCleft(target_id=drive_neuron.neuron_id, weight=0.5, phase_shift=0.0)
                    )
                    logger.debug(f"Linked Drive '{drive_constant.name}' to Concept '{word}'.")
