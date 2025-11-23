import logging
import asyncio
from logos.generation.serializer import Serializer
# Avoid circular import with LexicalTransducer if possible, but here we need it for type hint
# from cognition.transducer import LexicalTransducer

logger = logging.getLogger(__name__)

class InnerMonologue:
    """
    The Feedback Loop.
    Feeds the output of the Generator back into the Transducer.
    """
    def __init__(self, transducer, generator: Serializer):
        self.transducer = transducer
        self.generator = generator
        self.is_active = True # Default to active so it hears itself

    async def think_aloud(self, pvi):
        """
        Generates speech, then immediately listens to it.
        pvi: Pre-Verbal Intent dict
        """
        # 1. Speak
        text = self.generator.serialize(pvi)
        logger.info(f"INNER VOICE: '{text}'")
        
        # 2. Listen (Feedback)
        if self.is_active:
            # We "stream" our own thought back into our sensory cortex
            # This allows the AGI to reflect on what it just said.
            await self.transducer.stream_text(text)
