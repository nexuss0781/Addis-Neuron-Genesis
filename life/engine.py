import asyncio
import logging
from genesis import config

# --- Import Existing Systems ---
from neuro_cytoplasm.persistence import reanimate_organism
from neuro_mitochondria.engine import MetabolicEngine
from soma.interface import SomaticInterface
from psyche.engine import PsycheEngine
# ... (Previous Limbic/Volitional imports) ...
from volition.persona import PersonaEngine

# --- Import NEW Logos Systems ---
from logos.lexicon.polysemy import ContextTracker
from logos.lexicon.etymology import EtymologyEngine
from logos.lexicon.sensory import SynesthesiaMap
from logos.grammar.flow import SyntacticFlow
from logos.grammar.recursion import RecursionEngine
from logos.grammar.emergent import PatternHarvester
from logos.context.buffer import DiscourseBuffer
from logos.context.anaphora import AnaphoraResolver
from logos.generation.selector import LexicalSelector
from logos.generation.serializer import Serializer
from logos.social.mirror import SocialMirror
from logos.learning.gap_engine import GapEngine
from logos.ingestion.corpus_eater import CorpusEater
from logos.consciousness.monologue import InnerMonologue
# Import VectorSpace to init context
from logos.vector_space import SemanticSpace

# Import the GNW
from logos.consciousness.gnw import GlobalNeuronalWorkspace

logger = logging.getLogger(__name__)

class LifeEngine:
    """The Master Runtime Kernel."""
    def __init__(self, state_file):
        self.state_file = state_file
        self.c_graph, self.r_graph = reanimate_organism(state_file)
        
        # --- 1. Physics & Body ---
        self.psyche = PsycheEngine(self.r_graph, self.c_graph)
        self.metabolic = MetabolicEngine(self.c_graph, self.psyche, config.TICK_DURATION)
        self.psyche.metabolic_engine = self.metabolic
        self.soma = SomaticInterface()
        
        # --- 2. Limbic & Volition (Simplified init for brevity, assume previous logic) ---
        # self.hypo, self.drive... self.persona initialized here...

        # --- 3. LOGOS ARCHITECTURE (The Voice) ---
        self.sem_space = SemanticSpace() # Math
        self.context = ContextTracker(self.sem_space) # Polysemy
        self.etymology = EtymologyEngine() # Roots
        self.senses = SynesthesiaMap() # Feeling
        
        self.syntax_flow = SyntacticFlow() # Grammar Physics
        self.recursion = RecursionEngine() # Stack
        self.harvester = PatternHarvester(self.c_graph) # Learning
        
        self.discourse = DiscourseBuffer(self.sem_space) # Memory
        self.anaphora = AnaphoraResolver(self.discourse, self.c_graph) # Pronouns
        
        self.lex_selector = LexicalSelector(self.c_graph)
        self.serializer = Serializer(self.lex_selector) # Speech
        
        self.social = SocialMirror() # Empathy
        self.gap_engine = GapEngine(self.c_graph) # Curiosity

        # --- 4. CONSCIOUSNESS (The Spotlight) ---
        self.gnw = GlobalNeuronalWorkspace(self.c_graph)
        self.metabolic.gnw = self.gnw # Let the clock drive the GNW
        
        # The Transducer was in 'cognition', now wrapped by Monologue
        # (Assuming Transducer exists from Phase 1.8)
        from cognition.transducer import LexicalTransducer
        self.transducer = LexicalTransducer(self.c_graph, self.metabolic)

        self.monologue = InnerMonologue(self.transducer, self.serializer, self.gnw) # Consciousness

        self.corpus_eater = CorpusEater(self.c_graph) # Ingestion (Heavy tool, run on demand)

        logger.critical("LIFE ENGINE: Logos Systems online.")

    async def live(self):
        """The Life Cycle."""
        tasks = [
            self.metabolic.run(),
            self.psyche.monitor(),
            # ... start other monitors ...
            # Start Logos Monitors (if they have active loops)
            # e.g., self.monologue.monitor()
        ]
        
        await asyncio.gather(*tasks)
