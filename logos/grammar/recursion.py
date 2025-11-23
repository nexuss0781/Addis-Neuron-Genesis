import logging
from typing import List, Optional
from dataclasses import dataclass
from uuid import uuid4, UUID

logger = logging.getLogger(__name__)

@dataclass
class ContextFrame:
    """
    A snapshot of a grammatical context.
    """
    frame_id: UUID = uuid4()
    subject_id: Optional[UUID] = None
    verb_id: Optional[UUID] = None
    depth: int = 0

class RecursionEngine:
    """
    The Stack Memory. Handles nested clauses.
    """
    def __init__(self):
        self.stack: List[ContextFrame] = []
        self.max_depth = 5 # Sanity limit
        self._push_frame() # Root context
        logger.info("RecursionEngine initialized.")

    def _push_frame(self):
        depth = len(self.stack)
        if depth >= self.max_depth:
            logger.warning("RECURSION LIMIT: Sentence too complex.")
            return
        
        frame = ContextFrame(depth=depth)
        self.stack.append(frame)
        logger.debug(f"RECURSION: Pushed frame (Depth {depth})")

    def _pop_frame(self):
        if len(self.stack) > 1:
            self.stack.pop()
            logger.debug(f"RECURSION: Popped frame (Depth {len(self.stack)})")
    
    def process_trigger(self, word: str):
        """
        Checks if a word triggers a recursion event.
        """
        triggers_open = {"that", "which", "who", "because", "if", "("}
        triggers_close = {")", ".", ";"}
        
        if word in triggers_open:
            self._push_frame()
        elif word in triggers_close:
            # Reset to root on sentence end
            if word == ".":
                self.stack = [self.stack[0]]
            else:
                self._pop_frame()

    def get_current_context(self) -> ContextFrame:
        return self.stack[-1]
