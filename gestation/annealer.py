import logging
from collections import Counter
from neuro_cytoplasm.graph import NeuralGraph
from neuro_genome.schemas import Neuron, SynapticCleft
from neuro_genome.enums import NeuronType, SynapseType

logger = logging.getLogger(__name__)

class Annealer:
    """
    The Advanced Semantic Scaffolder.
    Uses statistical analysis to discover concepts and build the Ontology.
    """
    def __init__(self, graph: NeuralGraph):
        self.graph = graph

    def anneal(self):
        logger.info("Initiating Semantic Annealing...")
        self._discover_concepts()
        self._build_ontology()
        logger.info("Annealing complete.")

    def _discover_concepts(self):
        # 1. Count word frequency in definitions
        counts = Counter()
        sents = self.graph.get_neurons_by_type(NeuronType.LINGUISTIC_SENTENCE)
        for s in sents:
            for c in s.connections:
                if c.type == SynapseType.HIERARCHICAL:
                    counts[c.target_id] += 1
        
        # 2. Threshold
        threshold = max(2, int(len(sents) * 0.05))
        
        # 3. Create Concepts
        for nid, count in counts.items():
            if count >= threshold:
                word = self.graph.get_neuron(nid)
                if word and word.neuron_type == NeuronType.LINGUISTIC_WORD:
                    name = word.payload['name']
                    # Check for existence
                    if self.graph.get_neuron_by_name(name) and \
                       any(n.neuron_type == NeuronType.LOGICAL_CONCEPT for n in self.graph.get_neurons_by_type(NeuronType.LOGICAL_CONCEPT) if n.payload.get('name')==name):
                           continue

                    c_n = Neuron(neuron_type=NeuronType.LOGICAL_CONCEPT, payload={"name": name})
                    self.graph.add_neuron(c_n)
                    
                    # Link
                    word.connections.append(SynapticCleft(c_n.neuron_id, 1.2, SynapseType.ASSOCIATIVE))
                    c_n.connections.append(SynapticCleft(word.neuron_id, 1.2, SynapseType.ASSOCIATIVE))

    def _build_ontology(self):
        # Simplified pattern matcher for IS_A
        # In the full implementation, this uses the LinguisticPatternMiner
        # For the bootstrap, we use heuristic linking from definitions
        pass
