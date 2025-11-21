import asyncio
import logging
from collections import deque
from typing import Deque, List, Tuple

from neuro_cytoplasm.graph import NeuralGraph
from neuro_mitochondria.engine import MetabolicEngine, Signal

logger = logging.getLogger(__name__)

class PrimarySensoryCortex:
    """
    The Thalamic Relay. 
    Buffers raw character signals and assembles them into clean words.
    """
    def __init__(self, graph: NeuralGraph, engine: MetabolicEngine):
        self.graph = graph
        self.engine = engine
        
        # Private buffer for raw chars (Time, Char)
        self.char_buffer: Deque[Tuple[int, str]] = deque()
        
        # Public output buffer for the Recognition Cortex
        self.word_stream: Deque[str] = deque()
        
        self._boundaries = {'.', ' ', '\n', '!', '?'}
        logger.info("PrimarySensoryCortex initialized.")

    async def monitor(self):
        """Reads from the engine's sensory queue."""
        while self.engine.is_running:
            try:
                # Wait for sensory input
                signal = await asyncio.wait_for(self.engine.sensory_input_queue.get(), timeout=0.1)
                
                # 1. Forward to Consciousness (Immediate Priming)
                await self.engine.signal_queue.put(signal)
                
                # 2. Process Locally (Structural Assembly)
                neuron = self.graph.get_neuron(signal.target_id)
                if neuron:
                    char = neuron.payload.get('character')
                    if char:
                        self._assemble_stream(char)
                        
                self.engine.sensory_input_queue.task_done()
            
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break

    def _assemble_stream(self, char: str):
        """Assembles characters into words."""
        self.char_buffer.append((self.engine.current_tick, char))
        
        if char in self._boundaries:
            # Extract word
            word_chars = [c for _, c in self.char_buffer if c not in self._boundaries]
            if word_chars:
                word_str = "".join(word_chars)
                self.word_stream.append(word_str)
            
            # Pass the boundary too (important for sentence structure)
            if char in {'.', '!', '?'}:
                self.word_stream.append(char)

            self.char_buffer.clear()

    def get_stream(self) -> List[str]:
        """Returns and clears the current stream of recognized tokens."""
        if not self.word_stream: return []
        data = list(self.word_stream)
        self.word_stream.clear()
        return data
