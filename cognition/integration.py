import logging
import asyncio
from typing import List

from genesis import config
from neuro_cytoplasm.graph import NeuralGraph
from neuro_mitochondria.engine import MetabolicEngine
from neuro_genome.schemas import Neuron, SynapticCleft
from neuro_genome.enums import NeuronType, SynapseType
from .recognition import WordRecognitionCortex, RecognizedToken

logger = logging.getLogger(__name__)

class SemanticIntegrationEngine:
    """
    The Hippocampus.
    Binds words into thoughts and reinforces connections based on meaning.
    """
    def __init__(self, graph: NeuralGraph, engine: MetabolicEngine, cortex: WordRecognitionCortex):
        self.graph = graph
        self.engine = engine
        self.cortex = cortex
        self.buffer: List[RecognizedToken] = []
        logger.info("SemanticIntegrationEngine initialized.")

    async def monitor(self):
        while self.engine.is_running:
            try:
                token = await asyncio.wait_for(self.cortex.output_queue.get(), timeout=0.1)
                
                if token.is_boundary:
                    if self.buffer:
                        await self._crystallize_thought()
                    self.buffer = []
                else:
                    self.buffer.append(token)
                    
                self.cortex.output_queue.task_done()
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break

    async def _crystallize_thought(self):
        """
        1. Performs Spreading Activation & LTP.
        2. Creates the Gedanke Neuron.
        """
        word_neurons = [self.graph.get_neuron(t.neuron_id) for t in self.buffer]
        text_repr = " ".join([t.text for t in self.buffer])
        logger.debug(f"Integrating thought: '{text_repr}'")

        # --- 1. Semantic Resonance (LTP) ---
        activated_concepts = set()
        
        for i in range(len(word_neurons)):
            for j in range(i + 1, len(word_neurons)):
                n1 = word_neurons[i]
                n2 = word_neurons[j]
                
                # Check for existing connection
                cleft = next((c for c in n1.connections if c.target_id == n2.neuron_id), None)
                
                if cleft:
                    # Direct link exists: Strengthen it massively
                    cleft.weight += config.LEARNING_RATE * 5.0
                    activated_concepts.add(n1.neuron_id)
                    activated_concepts.add(n2.neuron_id)
                else:
                    # Check for shared neighbors (Indirect Resonance)
                    targets1 = {c.target_id for c in n1.connections}
                    targets2 = {c.target_id for c in n2.connections}
                    shared = targets1.intersection(targets2)
                    
                    if shared:
                        # They share a concept! Strengthen links to that concept.
                        activated_concepts.update(shared)
                        # Create a weak new association between the words
                        n1.connections.append(SynapticCleft(n2.neuron_id, config.LEARNING_RATE, SynapseType.ASSOCIATIVE))

        # --- 2. Gedanke Creation ---
        gedanke = Neuron(
            neuron_type=NeuronType.COGNITIVE_GEDANKE,
            payload={
                "text": text_repr,
                "sequence": [n.neuron_id for n in word_neurons]
            }
        )
        self.graph.add_neuron(gedanke)
        
        # Link Gedanke -> Words (Ordered)
        for i, wn in enumerate(word_neurons):
            w = 1.0 / (1.0 + i)
            gedanke.connections.append(SynapticCleft(wn.neuron_id, w, SynapseType.HIERARCHICAL))
            
        # Link Gedanke -> Concepts (Semantic)
        for cid in activated_concepts:
            gedanke.connections.append(SynapticCleft(cid, 0.5, SynapseType.ASSOCIATIVE))

        logger.info(f"GEDANKE FORMED: {gedanke.neuron_id}")
