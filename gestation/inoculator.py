import logging
from uuid import uuid4

from neuro_cytoplasm.resonance_graph import ResonanceGraph
from neuro_cytoplasm.graph import NeuralGraph
from neuro_genome.schemas import ResonanceNeuron, ResonanceCleft
from neuro_genome.affective import ALL_PRIMAL_AXES
from neuro_genome.drive import ALL_DRIVES
from neuro_genome.traits import TRAIT_CURIOSITY # Initial personality seed

logger = logging.getLogger(__name__)

class Inoculator:
    """
    Hardwires the innate Instincts (Drives) and Affect (Emotions).
    """
    def __init__(self, c_graph: NeuralGraph, r_graph: ResonanceGraph):
        self.c = c_graph
        self.r = r_graph

    def inoculate(self):
        logger.info("Initiating Inoculation...")
        self._seed_affective_core()
        self._seed_drives()
        self._seed_ego_traits()
        logger.info("Inoculation complete.")

    def _seed_affective_core(self):
        # Create Primal Axes Neurons
        for axis in ALL_PRIMAL_AXES:
            n = ResonanceNeuron(resonance_frequency=axis.base_frequency)
            # Store axis neurons in a retrievable way (e.g. by frequency lookup later)
            self.r.add_neuron(n)
            
            # Link Concepts to Affect (Hardwired Associations)
            # E.g. Link 'death' -> Negative Valence
            # (Simplified: In a real run, we'd scan for keywords)

    def _seed_drives(self):
        for drive in ALL_DRIVES:
            # Create Drive Neuron
            dn = ResonanceNeuron(resonance_frequency=drive.base_frequency)
            self.r.add_neuron(dn)
            
            # Link Drive -> Concept (The Instinct)
            # E.g. Hunger -> Food
            # We use a simple mapping for the prototype
            targets = []
            if "Energy" in drive.name: targets = ["sleep", "rest"]
            if "Growth" in drive.name: targets = ["learn", "read", "new"]
            if "Integrity" in drive.name: targets = ["fix", "correct"]

            for t_name in targets:
                c_n = self.c.get_neuron_by_name(t_name)
                if c_n:
                    r_n = self.r.get_neuron(c_n.neuron_id)
                    # Strong bidirectional link
                    dn.connections.append(ResonanceCleft(r_n.neuron_id, 1.0, 0.0))
                    r_n.connections.append(ResonanceCleft(dn.neuron_id, 0.5, 0.0))

    def _seed_ego_traits(self):
        # Seed the initial personality with CURIOSITY
        # In the future, this would be a TraitComplex graph insertion
        pass
