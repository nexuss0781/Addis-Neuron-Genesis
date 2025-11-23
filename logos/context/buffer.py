import logging
from collections import deque
from uuid import UUID
from typing import List, Optional

from logos.vector_space import Vector, SemanticSpace
from neuro_cytoplasm.graph import NeuralGraph

logger = logging.getLogger(__name__)

class DiscourseBuffer:
    """
    Short-term memory for the conversation.
    Tracks active entities and the overall 'Topic Vector'.
    """
    def __init__(self, space: SemanticSpace):
        self.space = space
        # Stores UUIDs of recently mentioned concepts (LIFO)
        self.entities: deque = deque(maxlen=20)
        # Stores Vectors of recent sentences
        self.topic_history: deque = deque(maxlen=5)
        self.current_topic = Vector([0.0]*5)

    def add_utterance(self, concept_ids: List[UUID], vector: Vector):
        """
        Updates state with a new sentence.
        """
        # 1. Update Entities
        for cid in concept_ids:
            # Move to front if exists (Recency)
            if cid in self.entities:
                self.entities.remove(cid)
            self.entities.appendleft(cid)
            
        # 2. Update Topic
        self.topic_history.append(vector)
        self.current_topic = self.space.get_centroid(list(self.topic_history))
        
    def get_recent_entities(self) -> List[UUID]:
        return list(self.entities)
