import logging
from typing import List, Tuple
from collections import Counter

from genesis import config
from neuro_cytoplasm.graph import NeuralGraph
from neuro_genome.schemas import Neuron
from neuro_genome.enums import NeuronType
from .flow import SyntacticFlow, SyntaxTag

logger = logging.getLogger(__name__)

class PatternHarvester:
    """
    The Observer. Scans text for low-energy grammatical patterns.
    """
    def __init__(self, graph: NeuralGraph):
        self.graph = graph
        self.physics = SyntacticFlow()
        self.observed_patterns = Counter()
        logger.info("PatternHarvester initialized.")

    def harvest(self):
        """
        Scans all sentences in memory.
        """
        sentences = self.graph.get_neurons_by_type(NeuronType.LINGUISTIC_SENTENCE)
        
        for sent in sentences:
            # 1. Extract POS Sequence
            # (Simplified: Assumes we can trace words -> POS)
            pos_seq = self._get_pos_sequence(sent)
            if not pos_seq: continue
            
            # 2. Analyze Energy
            energy = self.physics.analyze_flow(pos_seq)
            
            # 3. If efficient, record pattern
            if energy < 2.0: # Low energy threshold
                pattern_sig = tuple(t.name for t in pos_seq)
                self.observed_patterns[pattern_sig] += 1

    def crystallize_rules(self):
        """
        Converts frequent patterns into Rule Neurons.
        """
        THRESHOLD = 5 # Minimum observations
        
        for pattern, count in self.observed_patterns.items():
            if count >= THRESHOLD:
                rule_name = f"RULE:{'-'.join(pattern)}"
                if not self.graph.get_neuron_by_name(rule_name):
                    logger.info(f"GRAMMAR DISCOVERY: Crystallizing {rule_name} (Count: {count})")
                    
                    rule_neuron = Neuron(
                        neuron_type=NeuronType.LOGICAL_PATTERN,
                        payload={"name": rule_name, "pattern": pattern}
                    )
                    self.graph.add_neuron(rule_neuron)

    def _get_pos_sequence(self, sent_neuron: Neuron) -> List[SyntaxTag]:
        # This requires traversing the graph.
        # Placeholder logic for the blueprint:
        # 1. Get ordered word links from sent_neuron
        # 2. For each word, get its POS link
        # 3. Map POS string to SyntaxTag enum
        return []
