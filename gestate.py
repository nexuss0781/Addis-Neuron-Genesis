import logging
import os
from gestation.engine import GestationEngine

# Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DICT_PATH = os.path.join(BASE_DIR, "genesis_trinity/genesis/GenesisDictionary.yaml")
OUTPUT_PATH = "newborn.json.gz"

if __name__ == "__main__":
    if not os.path.exists(DICT_PATH):
        print(f"Error: Dictionary not found at {DICT_PATH}")
        exit(1)
        
    engine = GestationEngine(DICT_PATH)
    engine.gestate(OUTPUT_PATH)
