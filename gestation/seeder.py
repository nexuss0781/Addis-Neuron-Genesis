import logging
from typing import List, Dict, Any, Tuple
from uuid import UUID

from neuro_cytoplasm.graph import NeuralGraph
from neuro_genome.schemas import Neuron, SynapticCleft
from neuro_genome.enums import NeuronType, SynapseType

logger = logging.getLogger(__name__)

class PredictiveSeeder:
    """
    Orchestrates Neurogenesis.
    Builds the Cortical Columns (Words) and the Hierarchical Circuits (Alphabet Binding).
    """
    def __init__(self, graph: NeuralGraph, data: List[Dict]):
        self.graph = graph
        self.data = data
        self.alphabet_cache: Dict[str, UUID] = {}
        self.pos_cache: Dict[str, UUID] = {}

    def seed(self):
        logger.info("Initiating Predictive Seeding...")
        self._build_alphabet()
        self._build_words_and_circuits()
        self._link_definitions()
        self._link_relations()
        logger.info("Seeding complete.")

    def _build_alphabet(self):
        # Gather all chars
        chars = set()
        for entry in self.data:
            chars.update(entry['word'])
            for d in entry['definitions']: chars.update(d['text'])
        
        for char in sorted(list(chars)):
            if char not in self.alphabet_cache:
                n = Neuron(neuron_type=NeuronType.LINGUISTIC_ALPHABET, payload={"character": char, "name": f"char:{char}"})
                self.graph.add_neuron(n)
                self.alphabet_cache[char] = n.neuron_id

    def _build_words_and_circuits(self):
        # Create Words and wire the Predictive Circuit (Word <-> Alphabet)
        for entry in self.data:
            word_n = Neuron(
                neuron_type=NeuronType.LINGUISTIC_WORD,
                payload={
                    "name": entry['word'],
                    "lexical_id": entry['id'],
                    "language": entry['language']
                },
                # Inject Symbolic Vector if present
                symbolic_vector=entry.get('symbolic_seed')
            )
            self.graph.add_neuron(word_n)

            # --- The Circuit ---
            prev_char_id = None
            for i, char in enumerate(entry['word']):
                char_id = self.alphabet_cache[char]
                
                # 1. Top-Down Priming (Word -> Char)
                word_n.connections.append(SynapticCleft(char_id, 1.0, SynapseType.ASSOCIATIVE))
                
                # 2. Bottom-Up Recognition (Char -> Word)
                # Positional Weighting: First letters are more important
                w = 1.0 / (1.0 + i)
                char_n = self.graph.get_neuron(char_id)
                char_n.connections.append(SynapticCleft(word_n.neuron_id, w, SynapseType.HIERARCHICAL))

                # 3. Lateral Sequence (Char -> Char)
                if prev_char_id:
                    prev_n = self.graph.get_neuron(prev_char_id)
                    prev_n.connections.append(SynapticCleft(char_id, 1.0, SynapseType.ASSOCIATIVE))
                prev_char_id = char_id

    def _link_definitions(self):
        for entry in self.data:
            word_n = self.graph.get_neuron_by_name(entry['word'])
            if not word_n: continue

            for definition in entry['definitions']:
                # Create Sentence Neuron
                sent_n = Neuron(neuron_type=NeuronType.LINGUISTIC_SENTENCE, payload={"raw_text": definition['text']})
                self.graph.add_neuron(sent_n)
                
                # Link Word -> Definition
                word_n.connections.append(SynapticCleft(sent_n.neuron_id, 1.5, SynapseType.ASSOCIATIVE))

                # Link Definition -> Constituent Words (Hierarchical)
                # Simple tokenizer for Genesis
                words = definition['text'].lower().replace('.', '').split()
                for w in words:
                    target = self.graph.get_neuron_by_name(w)
                    if target:
                        sent_n.connections.append(SynapticCleft(target.neuron_id, 1.0, SynapseType.HIERARCHICAL))
                
                # Create POS Link
                pos = definition['pos'].upper()
                if pos not in self.pos_cache:
                    p_n = Neuron(neuron_type=NeuronType.LOGICAL_CONCEPT, payload={"name": f"POS:{pos}"})
                    self.graph.add_neuron(p_n)
                    self.pos_cache[pos] = p_n.neuron_id
                
                word_n.connections.append(SynapticCleft(self.pos_cache[pos], 1.0, SynapseType.HIERARCHICAL))

    def _link_relations(self):
        for entry in self.data:
            src = self.graph.get_neuron_by_name(entry['word'])
            if not src: continue

            for syn in entry.get('synonyms', []):
                tgt = self.graph.get_neuron_by_name(syn)
                if tgt:
                    src.connections.append(SynapticCleft(tgt.neuron_id, 0.8, SynapseType.ASSOCIATIVE))
                    tgt.connections.append(SynapticCleft(src.neuron_id, 0.8, SynapseType.ASSOCIATIVE))

            for ant in entry.get('antonyms', []):
                tgt = self.graph.get_neuron_by_name(ant)
                if tgt:
                    src.connections.append(SynapticCleft(tgt.neuron_id, -0.9, SynapseType.INHIBITORY))
                    tgt.connections.append(SynapticCleft(src.neuron_id, -0.9, SynapseType.INHIBITORY))
