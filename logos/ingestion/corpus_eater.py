import logging
import asyncio
import os
from typing import List

from neuro_cytoplasm.graph import NeuralGraph
from .hierarchy import HierarchicalBuilder

logger = logging.getLogger(__name__)

class CorpusEater:
    """
    The Book Eater.
    Ingests text files and uses the HierarchicalBuilder to construct
    the full 8-layer knowledge tower.
    """
    def __init__(self, graph: NeuralGraph):
        self.graph = graph
        self.builder = HierarchicalBuilder(graph)
        self.current_sentence_words: List = []
        
        # Config for segmentation
        self.PAGE_SIZE_PARAGRAPHS = 10

    async def ingest_library(self, library_path: str, topic_name: str):
        """
        Scans a folder structure. 
        Assumes folder name = Shelf Name.
        """
        logger.info(f"CORPUS: Scanning library at {library_path} for Topic: {topic_name}...")
        
        for root, dirs, files in os.walk(library_path):
            shelf_name = os.path.basename(root)
            if shelf_name == os.path.basename(library_path):
                shelf_name = "General"
                
            for filename in files:
                if filename.endswith(".txt") or filename.endswith(".md"):
                    book_title = os.path.splitext(filename)[0]
                    filepath = os.path.join(root, filename)
                    await self._ingest_book(filepath, book_title, shelf_name, topic_name)

    async def _ingest_book(self, filepath: str, title: str, shelf: str, topic: str):
        logger.info(f"CORPUS: Eating Book '{title}' from Shelf '{shelf}'...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            # Read line by line to handle massive files
            paragraph_buffer = []
            
            for line in f:
                line = line.strip()
                if not line:
                    # Empty line = Paragraph break
                    if paragraph_buffer:
                        await self._process_paragraph(" ".join(paragraph_buffer))
                        paragraph_buffer = []
                else:
                    paragraph_buffer.append(line)
            
            # Flush last paragraph
            if paragraph_buffer:
                await self._process_paragraph(" ".join(paragraph_buffer))
                
        # Finalize the Book
        book_neuron = self.builder.finalize_book(title, shelf, topic)
        logger.critical(f"CORPUS: Digested Book '{title}' (ID: {book_neuron.neuron_id})")

    async def _process_paragraph(self, text: str):
        """
        Breaks paragraph into sentences and words.
        """
        # Simple sentence splitting for now
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        
        for sent in sentences:
            if not sent.strip(): continue
            
            # Process Words
            words = sent.replace(',', '').split()
            word_neurons = []
            
            for word_str in words:
                # Level 1 & 2: Create/Get Word + Encoding
                wn = self.builder.process_word(word_str.lower())
                word_neurons.append(wn)
                
            # Level 3: Create Gedanke
            if word_neurons:
                self.builder.finalize_sentence(word_neurons)
        
        # Level 4: Create Paragraph
        para_neuron = self.builder.finalize_paragraph()
        
        # Check Page break logic
        if len(self.builder.current_paragraph_ids) >= self.PAGE_SIZE_PARAGRAPHS:
             # Level 5: Create Page
             self.builder.finalize_page()
             
        # Yield to event loop to prevent freezing
        await asyncio.sleep(0.01)
