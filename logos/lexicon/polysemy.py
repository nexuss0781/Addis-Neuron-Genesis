import logging
from uuid import UUID, uuid4
from typing import List, Dict, Optional

from neuro_genome.schemas import Neuron
from neuro_genome.enums import NeuronType
from logos.vector_space import Vector, SemanticSpace

logger = logging.getLogger(__name__)

class MeaningState:
    """
    Represents ONE specific definition of a polysemic word.
    (e.g., 'Bank' as a financial institution).
    """
    def __init__(self, definition_id: UUID, vector: Vector):
        self.definition_id = definition_id
        self.semantic_vector = vector
        # Probability of this meaning being the correct one (0.0 - 1.0)
        self.activation_probability = 0.0

class WordCloud:
    """
    The Quantum Container for a word string.
    Holds all potential meanings (states) of that word.
    """
    def __init__(self, word_string: str):
        self.word_string = word_string
        self.states: List[MeaningState] = []
        self.base_id = uuid4() # ID for the cloud itself

    def add_meaning(self, definition_id: UUID, vector: Vector):
        self.states.append(MeaningState(definition_id, vector))

    def collapse_wavefunction(self, context_vector: Vector) -> Optional[MeaningState]:
        """
        The Observer Effect.
        Uses the current Context Vector to determine which meaning is most likely.
        Returns the winning MeaningState.
        """
        if not self.states: return None
        if len(self.states) == 1: return self.states[0] # Unambiguous

        best_state = None
        max_similarity = -1.0

        for state in self.states:
            # How close is this meaning to the current conversation context?
            similarity = state.semantic_vector.cosine_similarity(context_vector)
            state.activation_probability = similarity
            
            if similarity > max_similarity:
                max_similarity = similarity
                best_state = state
        
        # If the context match is very weak, we might return the "dominant" (first) meaning
        # or None to signal confusion. For now, we return the best match.
        return best_state

class ContextTracker:
    """
    Maintains the 'Current Semantic Context Vector' of the conversation.
    This is the reference point for collapsing polysemy.
    """
    def __init__(self, space: SemanticSpace):
        self.space = space
        # A rolling window of recent vectors
        self.history: List[Vector] = []
        self.window_size = 10
        # Start with a neutral vector
        self.current_context = Vector([0.0] * 5) 

    def update(self, vector: Vector):
        """Adds a new concept vector to the context history."""
        self.history.append(vector)
        if len(self.history) > self.window_size:
            self.history.pop(0)
        
        # Recalculate the centroid
        self.current_context = self.space.get_centroid(self.history)
        
    def get_context(self) -> Vector:
        return self.current_context
