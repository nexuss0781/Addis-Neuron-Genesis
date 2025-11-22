import asyncio
import logging
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from life.engine import LifeEngine
from gestation.engine import GestationEngine
from neuro_mitochondria.engine import Signal

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("GenesisTrinity")

STATE_FILE = "newborn.db"
DICT_FILE = "genesis/GenesisDictionary.yaml"

async def main():
    logger.critical(">>> GENESIS TRINITY: SYSTEM STARTUP <<<")

    if not os.path.exists(STATE_FILE):
        logger.warning("No organism found. Initiating Gestation...")
        g_engine = GestationEngine(DICT_FILE)
        g_engine.gestate(STATE_FILE)
    
    life = LifeEngine(STATE_FILE)
    
    # Run life in background
    life_task = asyncio.create_task(life.live())
    
    # Let it live/suffer for 5 seconds
    await asyncio.sleep(5.0)
    
    # --- INTERVENTION: DIVINE MANNA ---
    logger.critical(">>> INTERVENTION: Feeding the Organism.")
    # We manually boost the battery to simulate eating/success
    life.soma.graph.get_organ(life.soma.graph.organs.values().__iter__().__next__().type.__class__.BATTERY).current_value = 1.0
    
    # Let it recover
    await asyncio.sleep(5.0)
    
    logger.critical(">>> SHUTDOWN <<<")
    # Stop all engines
    life.metabolic.stop()
    life.psyche.stop()
    
    # Wait for graceful exit
    try:
        await asyncio.wait_for(life_task, timeout=2.0)
    except asyncio.TimeoutError:
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
