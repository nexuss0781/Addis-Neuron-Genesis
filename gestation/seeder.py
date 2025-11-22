import logging
from typing import List, Dict, Any, Tuple, Generator
from uuid import UUID

from neuro_cytoplasm.graph import NeuralGraph
from neuro_genome.schemas import Neuron, SynapticCleft
from neuro_genome.enums import NeuronType, SynapseType
# CORRECTED IMPORT
from neuro_genome.utils.word_encoder import WordEncoder

logger = logging.getLogger(__name__)

class PredictiveSeeder:
    """
    Orchestrates Neurogenesis.
    """
    def __init__(self, graph: NeuralGraph, data: Generator[Dict, None, None] | List[Dict]):
        self.graph = graph
        # If data is a generator, convert it to a list for multi-pass seeding.
        if isinstance(data, Generator):
            logger.info("Converting dictionary stream to list for multi-pass seeding...")
            self.data = list(data)
            logger.info(f"Dictionary list created with {len(self.data)} entries.")
        else:
            self.data = data
        self.alphabet_cache: Dict[str, UUID] = {}
        self.pos_cache: Dict[str, UUID] = {}

    def seed(self):
        logger.info(f"Initiating Predictive Seeding with {len(self.data)} entries...")
        self._build_alphabet()
        self._build_words_and_circuits()
        self._link_definitions()
        self._link_relations()
        logger.info("Seeding complete.")

    def _build_alphabet(self):
        chars = set()
        for i, entry in enumerate(self.data):
            if i % 10000 == 0 and i > 0:
                logger.info(f"Alphabet building: Processed {i} entries...")
            chars.update(entry['word'])
            for d in entry['definitions']: chars.update(d['text'])
        
        for i, char in enumerate(sorted(list(chars))):
            if i % 50 == 0 and i > 0:
                logger.info(f"Alphabet built: {i} characters so far...")
            if char not in self.alphabet_cache:
                n = Neuron(neuron_type=NeuronType.LINGUISTIC_ALPHABET, payload={"character": char, "name": f"char:{char}"})
                self.graph.add_neuron(n)
                self.alphabet_cache[char] = n.neuron_id

    def _build_words_and_circuits(self):
        # Use the shared WordEncoder for consistency
        encoder = WordEncoder(self.graph, self.alphabet_cache)
        
        for i, entry in enumerate(self.data):
            if i % 10000 == 0 and i > 0:
                logger.info(f"Word building: Processed {i} entries...")
            word_n = Neuron(
                neuron_type=NeuronType.LINGUISTIC_WORD,
                payload={
                    "name": entry['word'],
                    "lexical_id": entry['id'],
                    "language": entry['language']
                },
                symbolic_vector=entry.get('symbolic_seed')
            )
            self.graph.add_neuron(word_n)
            
            # Use the encoder
            encoder.encode_word(word_n)

    def _link_definitions(self):
        for i, entry in enumerate(self.data):
            if i % 10000 == 0 and i > 0:
                logger.info(f"Definition linking: Processed {i} entries...")
            word_n = self.graph.get_neuron_by_name(entry['word'])
            if not word_n: continue

            for definition in entry['definitions']:
                sent_n = Neuron(neuron_type=NeuronType.LINGUISTIC_SENTENCE, payload={"raw_text": definition['text']})
                self.graph.add_neuron(sent_n)
                
                word_n.connections.append(SynapticCleft(sent_n.neuron_id, 1.5, SynapseType.ASSOCIATIVE))

                words = definition['text'].lower().replace('.', '').split()
                for w in words:
                    target = self.graph.get_neuron_by_name(w)
                    if target:
                        sent_n.connections.append(SynapticCleft(target.neuron_id, 1.0, SynapseType.HIERARCHICAL))
                
                pos = definition['pos'].upper()
                if pos not in self.pos_cache:
                    p_n = Neuron(neuron_type=NeuronType.LOGICAL_CONCEPT, payload={"name": f"POS:{pos}"})
                    self.graph.add_neuron(p_n)
                    self.pos_cache[pos] = p_n.neuron_id
                
                word_n.connections.append(SynapticCleft(self.pos_cache[pos], 1.0, SynapseType.HIERARCHICAL))

    def _link_relations(self):
        for i, entry in enumerate(self.data):
            if i % 10000 == 0 and i > 0:
                logger.info(f"Relation linking: Processed {i} entries...")
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
