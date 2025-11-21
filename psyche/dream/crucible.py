import logging
from neuro_genome.schemas import Neuron, SynapticCleft
from neuro_genome.enums import NeuronType, SynapseType

logger = logging.getLogger(__name__)

class SynthesisCrucible:
    """The Alchemical Reactor."""
    def __init__(self, canvas):
        self.canvas = canvas

    def fuse(self):
        # Find top 2 active concepts
        active = sorted(
            [n for n in self.canvas.sandbox.values() if n.neuron_type == NeuronType.LOGICAL_CONCEPT],
            key=lambda x: x.nap, reverse=True
        )
        if len(active) < 2: return None

        a, b = active[0], active[1]
        if a.nap > 1.5 and b.nap > 1.5:
            name = f"DREAM:{a.payload['name']}+{b.payload['name']}"
            logger.critical(f"DREAM SYNTHESIS: Fusing {a.payload['name']} + {b.payload['name']}")
            
            new_n = Neuron(neuron_type=NeuronType.LOGICAL_CONCEPT, payload={"name": name})
            new_n.connections.append(SynapticCleft(a.neuron_id, 1.0, SynapseType.HIERARCHICAL))
            new_n.connections.append(SynapticCleft(b.neuron_id, 1.0, SynapseType.HIERARCHICAL))
            self.canvas.add(new_n)
            return new_n
        return None
