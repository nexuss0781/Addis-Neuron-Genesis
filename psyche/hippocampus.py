import asyncio
import logging
from typing import Set
from uuid import UUID

from genesis import config
from neuro_genome.schemas import ResonanceCleft
from neuro_genome.enums import NeuronType
from .engine import PsycheEngine
from neuro_mitochondria.engine import MetabolicEngine

logger = logging.getLogger(__name__)

class HippocampusEngine:
    """
    The Emotional Memory Binder.
    It connects "What happened" (Conscious) with "How it felt" (Subconscious).
    """
    def __init__(self, psyche: PsycheEngine, metabolic: MetabolicEngine):
        self.psyche = psyche
        self.metabolic = metabolic
        self.processed_emotions: Set[UUID] = set()
        logger.info("HippocampusEngine initialized.")

    async def monitor(self):
        while self.psyche.is_running:
            await self._bind_memories()
            await asyncio.sleep(config.TICK_DURATION * 10)

    async def _bind_memories(self):
        # Scan for new Emotions (Resonance Neurons that act as hubs)
        # In this implementation, we identify them by their lack of connections to concepts
        # or simply by tracking what we've seen.
        
        # Identify potential emotion neurons: 
        # They are REOSNANCE_NODE type but NOT Primal Axes (which we know are fixed).
        # We filter out axes by checking if they are in the genome list.
        
        # (Optimization: In a real system, Amygdala would emit an event. 
        # Here we scan the graph for robustness.)
        
        for r_id, r_neuron in self.psyche.r_graph._neurons.items():
            if r_id in self.processed_emotions: continue
            
            # Heuristic: New emotions have connections TO axes but not FROM concepts yet.
            if not r_neuron.connections: continue 
            
            # If it's a valid emotion candidate...
            self._process_emotion(r_neuron)

    def _process_emotion(self, emotion_neuron):
        # 1. Search for Cause
        # Look back in the conscious firing trace
        trace = list(self.metabolic.firing_trace)
        cause_id = None
        
        # We look for the most recent HIGH-LEVEL concept (Logical or Linguistic)
        for tick, nid in reversed(trace):
            if self.metabolic.current_tick - tick > 20: break # Too old
            
            c_neuron = self.metabolic.graph.get_neuron(nid)
            if c_neuron and c_neuron.neuron_type in [NeuronType.LOGICAL_CONCEPT, NeuronType.LINGUISTIC_WORD]:
                cause_id = nid
                break
        
        if cause_id:
            # 2. Forge the Link
            # We link the Concept's TWIN to the Emotion.
            # Note: Concept ID == Twin ID.
            twin_neuron = self.psyche.r_graph.get_neuron(cause_id)
            
            if twin_neuron:
                logger.warning(f"HIPPOCAMPUS: Binding Emotion {emotion_neuron.neuron_id} to Concept {cause_id}.")
                
                # Bidirectional Resonance
                # Concept -> Emotion (Recall triggers feeling)
                twin_neuron.connections.append(ResonanceCleft(emotion_neuron.neuron_id, 1.0, 0.0))
                # Emotion -> Concept (Feeling triggers recall)
                emotion_neuron.connections.append(ResonanceCleft(twin_neuron.neuron_id, 0.5, 0.0))
                
        self.processed_emotions.add(emotion_neuron.neuron_id)
