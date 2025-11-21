import logging
import asyncio
from dataclasses import dataclass
from uuid import UUID

from genesis_trinity import config
from neuro_cytoplasm.graph import NeuralGraph
from neuro_mitochondria.engine import MetabolicEngine, Signal
from neuro_genome.schemas import Neuron
from neuro_genome.enums import NeuronType
from genesis.seeder import WordEncoder # Re-using the logic from gestation
from .sensory import PrimarySensoryCortex

logger = logging.getLogger(__name__)

@dataclass
class RecognizedToken:
    """A resolved linguistic unit."""
    neuron_id: UUID
    text: str
    is_boundary: bool = False

class WordRecognitionCortex:
    """
    Wernicke's Area.
    Recognizes known words and dynamically learns unknown ones.
    """
    def __init__(self, graph: NeuralGraph, engine: MetabolicEngine, sensory: PrimarySensoryCortex):
        self.graph = graph
        self.engine = engine
        self.sensory = sensory
        
        # Output stream for the Integration Engine
        self.output_queue: asyncio.Queue[RecognizedToken] = asyncio.Queue()
        
        # Cache for alphabet (needed for dynamic encoding)
        self._alphabet_cache = {}
        for n in self.graph.get_neurons_by_type(NeuronType.LINGUISTIC_ALPHABET):
            self._alphabet_cache[n.payload['character']] = n.neuron_id
            
        logger.info("WordRecognitionCortex initialized.")

    async def monitor(self):
        while self.engine.is_running:
            tokens = self.sensory.get_stream()
            
            for token_str in tokens:
                if token_str in {'.', '!', '?'}:
                    # It's a sentence boundary
                    await self.output_queue.put(RecognizedToken(None, token_str, is_boundary=True))
                    continue

                # It's a word
                neuron = self.graph.get_neuron_by_name(token_str)
                
                if not neuron:
                    # UNKNOWN WORD -> Dynamic Growth
                    neuron = self._learn_new_word(token_str)
                
                # Fire the word neuron (Recognition)
                await self.engine.signal_queue.put(
                    Signal(neuron.neuron_id, neuron.neuron_id, 1.0)
                )
                
                # Pass to Integration
                await self.output_queue.put(
                    RecognizedToken(neuron.neuron_id, token_str)
                )

            await asyncio.sleep(config.TICK_DURATION)

    def _learn_new_word(self, text: str) -> Neuron:
        logger.info(f"VOCABULARY GROWTH: Learning new word '{text}'")
        neuron = Neuron(
            neuron_type=NeuronType.LINGUISTIC_WORD,
            payload={"name": text}
        )
        self.graph.add_neuron(neuron)
        
        # Build the circuit immediately
        encoder = WordEncoder(self.graph, self._alphabet_cache)
        encoder.encode_word(neuron)
        
        return neuron
