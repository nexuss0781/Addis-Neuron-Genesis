import asyncio
import logging
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from genesis_engine import GenesisEngine
from neuro_cytoplasm.persistence import hibernate_organism

# --- Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("VastGenesis")

# --- Asset Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# WARNING: Ensure 'dictionary.json' is placed in the root or updated path
DICT_PATH = os.path.join(BASE_DIR, "dictionary.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "vast_mind.json.gz")

def main():
    logger.critical(f">>> INITIATING VAST GENESIS PROTOCOL <<<")
    logger.info(f"Source: {DICT_PATH}")
    logger.info(f"Target: {OUTPUT_PATH}")
    
    if not os.path.exists(DICT_PATH):
        logger.error("CRITICAL: dictionary.json not found! Please place the file.")
        return

    engine = GenesisEngine(DICT_PATH)
    
    # Run the genesis (synchronous part)
    c_graph, r_graph = engine.run_genesis()
    
    # Save the result
    logger.info("Hibernating Vast Mind... (This may take time)")
    hibernate_organism(c_graph, r_graph, OUTPUT_PATH)
    logger.critical(">>> VAST GENESIS COMPLETE <<<")

if __name__ == "__main__":
    main()
