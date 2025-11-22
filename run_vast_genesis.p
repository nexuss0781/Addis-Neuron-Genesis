import logging
import os
import sys

# We are in ~/genesis_trinity.
# Imports work directly from the current directory.
from genesis.genesis_engine import GenesisEngine
from neuro_cytoplasm.persistence import hibernate_organism

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("VastGenesis")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DICT_PATH = os.path.join(BASE_DIR, "dictionary.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "vast_mind.json.gz")

def main():
    logger.critical(f">>> INITIATING VAST GENESIS PROTOCOL <<<")
    
    if not os.path.exists(DICT_PATH):
        logger.error(f"CRITICAL: {DICT_PATH} not found!")
        # Create dummy for test
        with open(DICT_PATH, "w") as f:
             f.write('[{"word":"test","pos":"n.","definitions":["A test"],"synonyms":"trial"}]')
        logger.warning("Created dummy dictionary.json")

    engine = GenesisEngine(DICT_PATH)
    c_graph, r_graph = engine.run_genesis()
    
    logger.info("Hibernating Vast Mind...")
    hibernate_organism(c_graph, r_graph, OUTPUT_PATH)
    logger.critical(">>> VAST GENESIS COMPLETE <<<")

if __name__ == "__main__":
    main()
