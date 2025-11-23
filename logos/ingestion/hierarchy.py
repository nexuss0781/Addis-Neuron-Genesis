import logging
from uuid import uuid4
from typing import List

from neuro_cytoplasm.graph import NeuralGraph
from neuro_genome.schemas import Neuron, SynapticCleft
from neuro_genome.enums import NeuronType, SynapseType

# Import the WordEncoder to ensure low-level structure
from neuro_genome.utils.word_encoder import WordEncoder

logger = logging.getLogger(__name__)

class HierarchicalBuilder:
    """
    The Architect of the Tower.
    Constructs the full vertical hierarchy from raw text stream.
    """
    def __init__(self, graph: NeuralGraph):
        self.graph = graph
        self.encoder = None # Will init with alphabet cache
        
        # Buffers for the hierarchy
        self.current_gedanke_ids: List[uuid4] = [] # Sentences -> Paragraph
        self.current_paragraph_ids: List[uuid4] = [] # Paragraphs -> Page
        self.current_page_ids: List[uuid4] = [] # Pages -> Book
        
        logger.info("HierarchicalBuilder initialized.")

    def _ensure_encoder(self):
        if not self.encoder:
            # Build cache for WordEncoder
            cache = {
                n.payload['character']: n.neuron_id 
                for n in self.graph.get_neurons_by_type(NeuronType.LINGUISTIC_ALPHABET)
            }
            self.encoder = WordEncoder(self.graph, cache)

    def process_word(self, word_str: str) -> Neuron:
        """
        Level 1 & 2: Alphabet -> Word
        """
        self._ensure_encoder()
        
        # 1. Check/Create Word Neuron
        word_neuron = self.graph.get_neuron_by_name(word_str)
        if not word_neuron:
            word_neuron = Neuron(
                neuron_type=NeuronType.LINGUISTIC_WORD,
                payload={"name": word_str}
            )
            self.graph.add_neuron(word_neuron)
            
            # 2. Apply Alphabet Encoding (The Bond)
            # This links the Word to the Alphabet neurons and creates the pattern
            self.encoder.encode_word(word_neuron)
            
        return word_neuron

    def finalize_sentence(self, word_neurons: List[Neuron]) -> Neuron:
        """
        Level 3: Word -> Gedanke (Sentence)
        """
        # Create the Thought-Form
        gedanke = Neuron(
            neuron_type=NeuronType.COGNITIVE_GEDANKE,
            payload={"text_preview": " ".join([n.payload['name'] for n in word_neurons[:5]]) + "..."}
        )
        self.graph.add_neuron(gedanke)
        
        # Link Gedanke -> Words (Ordered)
        for i, w in enumerate(word_neurons):
            # Positional Weighting
            weight = 1.0 / (1.0 + i)
            gedanke.connections.append(SynapticCleft(w.neuron_id, weight, SynapseType.HIERARCHICAL))
            
        self.current_gedanke_ids.append(gedanke.neuron_id)
        return gedanke

    def finalize_paragraph(self) -> Neuron:
        """
        Level 4: Gedanke -> Paragraph
        Triggered by double newline or max sentences.
        """
        if not self.current_gedanke_ids: return None
        
        para = Neuron(neuron_type=NeuronType.LINGUISTIC_PARAGRAPH)
        self.graph.add_neuron(para)
        
        for gid in self.current_gedanke_ids:
            para.connections.append(SynapticCleft(gid, 1.0, SynapseType.HIERARCHICAL))
            
        self.current_gedanke_ids = [] # Clear buffer
        self.current_paragraph_ids.append(para.neuron_id)
        return para

    def finalize_page(self) -> Neuron:
        """
        Level 5: Paragraph -> Page
        Triggered by token count or explicit page break.
        """
        if not self.current_paragraph_ids: return None
        
        page = Neuron(neuron_type=NeuronType.LINGUISTIC_PAGE)
        self.graph.add_neuron(page)
        
        for pid in self.current_paragraph_ids:
            page.connections.append(SynapticCleft(pid, 1.0, SynapseType.HIERARCHICAL))
            
        self.current_paragraph_ids = []
        self.current_page_ids.append(page.neuron_id)
        return page

    def finalize_book(self, title: str, shelf_name: str, topic_name: str) -> Neuron:
        """
        Level 6, 7, 8: Page -> Book -> Shelf -> Topic
        Triggered at end of file.
        """
        # 1. Create Book
        if self.current_paragraph_ids: self.finalize_page() # Flush remaining
        
        book = Neuron(neuron_type=NeuronType.LINGUISTIC_BOOK, payload={"name": title})
        self.graph.add_neuron(book)
        
        for pid in self.current_page_ids:
            book.connections.append(SynapticCleft(pid, 1.0, SynapseType.HIERARCHICAL))
            
        # 2. Link to Shelf
        shelf = self._get_or_create_node(shelf_name, NeuronType.LINGUISTIC_SHELF)
        shelf.connections.append(SynapticCleft(book.neuron_id, 1.0, SynapseType.HIERARCHICAL))
        
        # 3. Link Shelf to Topic
        topic = self._get_or_create_node(topic_name, NeuronType.LOGICAL_CONCEPT) # Topics are Concepts
        topic.connections.append(SynapticCleft(shelf.neuron_id, 1.0, SynapseType.HIERARCHICAL))
        
        self.current_page_ids = []
        return book

    def _get_or_create_node(self, name, n_type):
        node = self.graph.get_neuron_by_name(name)
        if not node:
            node = Neuron(neuron_type=n_type, payload={"name": name})
            self.graph.add_neuron(node)
        return node
