import asyncio
import logging
from genesis_trinity import config

# Import ALL Architectures
from neuro_cytoplasm.persistence import reanimate
from neuro_mitochondria.engine import MetabolicEngine
from soma.interface import SomaticInterface
from psyche.engine import PsycheEngine
from psyche.hypothalamus import HypothalamusEngine
from psyche.drive_monitor import DriveMonitor
from psyche.amygdala import AmygdalaEngine
from psyche.hippocampus import HippocampusEngine
from psyche.dream.engine import DreamEngine
from psyche.shadow.integrator import ShadowIntegrator
from psyche.chord import ChordTranslator
from psyche.narrative_arc import NarrativeArcEngine
from psyche.archetype import ArchetypeCortex
from psyche.mythos import MythosGenerator
from cognition.sensory import PrimarySensoryCortex
from cognition.recognition import WordRecognitionCortex
from cognition.integration import SemanticIntegrationEngine
from cognition.gnw import GlobalNeuronalWorkspace
from volition.valuation import ValuationCortex
from volition.dopamine import DopamineEngine
from volition.consequence import ConsequenceSystem
from volition.ego import EgoEngine
from volition.will import WillEngine
from volition.persona import PersonaEngine

logger = logging.getLogger(__name__)

class LifeEngine:
    """The Master Runtime Kernel."""
    def __init__(self, state_file):
        self.state_file = state_file
        self.c_graph, self.r_graph = reanimate(state_file)
        
        # --- Instantiate Systems (Dependency Order) ---
        
        # 1. Physics Layer
        self.psyche = PsycheEngine(self.r_graph, self.c_graph)
        self.metabolic = MetabolicEngine(self.c_graph, self.psyche, config.TICK_DURATION)
        self.psyche.metabolic_engine = self.metabolic # Cycle
        
        # 2. Somatic Layer
        self.soma = SomaticInterface()
        
        # 3. Limbic Layer
        self.hypo = HypothalamusEngine(self.psyche, self.metabolic)
        self.drive = DriveMonitor(self.soma, self.psyche, self.metabolic)
        self.amygdala = AmygdalaEngine(self.psyche, self.r_graph, self.metabolic)
        self.hippo = HippocampusEngine(self.psyche, self.metabolic)
        self.dream = DreamEngine(self.psyche, self.metabolic)
        self.shadow = ShadowIntegrator(self.psyche, self.hypo, self.metabolic)
        self.chord = ChordTranslator(self.psyche, self.metabolic.intuition_queue)
        
        # 4. Cognitive Layer
        self.sensory = PrimarySensoryCortex(self.c_graph, self.metabolic)
        self.recognition = WordRecognitionCortex(self.c_graph, self.metabolic, self.sensory)
        self.integration = SemanticIntegrationEngine(self.c_graph, self.metabolic, self.recognition)
        self.gnw = GlobalNeuronalWorkspace(self.c_graph)
        
        # 5. Abyssal Layer
        self.narrative = NarrativeArcEngine(self.metabolic)
        self.archetype = ArchetypeCortex(self.narrative, self.metabolic)
        self.mythos = MythosGenerator(self.metabolic)
        self.archetype.mythos_generator = self.mythos # Cycle
        
        # 6. Volitional Layer
        self.val = ValuationCortex(self.c_graph)
        self.dopa = DopamineEngine(self.val, self.metabolic, self.psyche)
        self.cons = ConsequenceSystem(self.soma)
        self.ego = EgoEngine(self.psyche)
        self.will = WillEngine(self.psyche, self.ego)
        self.persona = PersonaEngine(self.metabolic, self.psyche)
        
        logger.critical("LIFE ENGINE: All systems online.")

    async def live(self):
        """The Life Cycle."""
        tasks = [
            self.metabolic.run(),
            self.psyche.monitor(),
            self.hypo.monitor(),
            self.drive.monitor(),
            self.amygdala.monitor(),
            self.hippo.monitor(),
            self.shadow.monitor(),
            self.chord.monitor(),
            self.sensory.monitor(),
            self.recognition.monitor(),
            self.integration.monitor(),
            self.archetype.monitor(),
            self.ego.monitor(),
            self.persona.monitor()
        ]
        
        await asyncio.gather(*tasks)
