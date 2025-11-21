import logging
import os

from neuro_cytoplasm.graph import NeuralGraph
from neuro_cytoplasm.resonance_graph import ResonanceGraph
from neuro_cytoplasm.persistence import hibernate_organism

from .transcriber import GeneticTranscriber
from .seeder import PredictiveSeeder
from .twin_forge import TwinForge
from .inoculator import Inoculator
from .annealer import Annealer

logger = logging.getLogger(__name__)

class GestationEngine:
    def __init__(self, dictionary_path: str):
        self.dict_path = dictionary_path
        self.c_graph = NeuralGraph()
        self.r_graph = ResonanceGraph()

    def gestate(self, output_path: str):
        logger.critical("=== GESTATION PROTOCOL INITIATED ===")
        
        # 1. Transcribe
        transcriber = GeneticTranscriber()
        genome_data = transcriber.parse(self.dict_path)
        
        # 2. Seed (Conscious)
        seeder = PredictiveSeeder(self.c_graph, genome_data)
        seeder.seed()
        
        # 3. Anneal (Conscious Structure)
        annealer = Annealer(self.c_graph)
        annealer.anneal()
        
        # 4. Twin (Subconscious)
        forge = TwinForge(self.c_graph, self.r_graph)
        forge.forge()
        
        # 5. Inoculate (Instincts)
        inoculator = Inoculator(self.c_graph, self.r_graph)
        inoculator.inoculate()
        
        # 6. Birth
        logger.critical(f"GESTATION COMPLETE. Newborn created with {len(self.c_graph)} conscious neurons and {len(self.r_graph)} subconscious neurons.")
        hibernate_organism(self.c_graph, self.r_graph, output_path)
