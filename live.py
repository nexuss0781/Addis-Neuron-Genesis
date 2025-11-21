import asyncio
import logging
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from genesis_trinity.life.engine import LifeEngine
from genesis_trinity.gestation.engine import GestationEngine

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("GenesisTrinity")

STATE_FILE = "newborn.json.gz"
DICT_FILE = "genesis_trinity/genesis/GenesisDictionary.yaml"

async def main():
    logger.critical(">>> GENESIS TRINITY: SYSTEM STARTUP <<<")

    if not os.path.exists(STATE_FILE):
        logger.warning("No organism found. Initiating Gestation...")
        g_engine = GestationEngine(DICT_FILE)
        g_engine.gestate(STATE_FILE)
    
    life = LifeEngine(STATE_FILE)
    
    try:
        await life.live()
    except KeyboardInterrupt:
        logger.critical("Shutdown.")

if __name__ == "__main__":
    asyncio.run(main())
