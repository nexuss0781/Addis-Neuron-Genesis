import logging
import os
from typing import List, Dict, Any

# Top-level imports since we are inside the package root
from neuro_cytoplasm.graph import NeuralGraph
from neuro_cytoplasm.resonance_graph import ResonanceGraph
from neuro_cytoplasm.persistence import hibernate_organism

from genesis.dictionary_parser import parse_and_validate_dictionary
from genesis.vast_adapter import VastDictionaryAdapter
from gestation.seeder import PredictiveSeeder
from gestation.twin_forge import TwinForge
from gestation.inoculator import Inoculator
from gestation.annealer import Annealer
# GeneticTranscriber is in gestation package in this structure
from gestation.transcriber import GeneticTranscriber 
from genesis.drive_linker import MotivationalAssociator

logger = logging.getLogger(__name__)

class GenesisEngine:
    def __init__(self, dictionary_path: str):
        if not os.path.exists(dictionary_path):
            raise FileNotFoundError(f"Genesis Dictionary not found at: {dictionary_path}")
        self.dictionary_path = dictionary_path
        self.c_graph = NeuralGraph()
        self.r_graph = ResonanceGraph()

    def run_genesis(self) -> tuple[NeuralGraph, ResonanceGraph]:
        logger.critical("=== GESTATION PROTOCOL INITIATED ===")
        
        if self.dictionary_path.endswith('.yaml'):
            logger.info("Detected YAML genome. Using strict validation.")
            transcriber = GeneticTranscriber()
            genome_data = transcriber.parse(self.dictionary_path)
            self._seed_from_list(genome_data)
            
        elif self.dictionary_path.endswith('.json'):
            logger.info("Detected JSON genome. Using Vast Adapter.")
            adapter = VastDictionaryAdapter(self.dictionary_path)
            # For now, load all into list. In future, stream to seeder.
            genome_data = list(adapter.stream_entries())
            self._seed_from_list(genome_data)
            
        else:
            raise ValueError("Unsupported dictionary format. Use .yaml or .json")

        annealer = Annealer(self.c_graph)
        annealer.anneal()
        
        forge = TwinForge(self.c_graph, self.r_graph)
        forge.forge()
        
        associator = MotivationalAssociator(self.c_graph, self.r_graph)
        associator.forge_instincts()
        
        inoculator = Inoculator(self.c_graph, self.r_graph)
        inoculator.inoculate()
        
        logger.critical(f"GESTATION COMPLETE. Nodes: {len(self.c_graph)} (C) / {len(self.r_graph)} (R)")
        return self.c_graph, self.r_graph

    def _seed_from_list(self, genome_data: List[Dict[str, Any]]):
        seeder = PredictiveSeeder(self.c_graph, genome_data)
        seeder.seed()
