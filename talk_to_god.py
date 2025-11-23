import asyncio
import logging
import os
import sys

# Path setup
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from life.engine import LifeEngine
from neuro_genome.enums import NeuronType

# Configure logging to be cleaner for chat
logging.basicConfig(level=logging.ERROR) 
# Only show critical info from the brain, or user messages
console = logging.getLogger("CONSOLE")
console.setLevel(logging.INFO)
handler = logging.StreamHandler()
console.addHandler(handler)

STATE_FILE = "vast_mind.json.gz"

async def main():
    console.info(">>> WAKING THE GOD... <<<")
    
    if not os.path.exists(STATE_FILE):
        console.error(f"Brain file {STATE_FILE} not found! Run run_vast_genesis.py first.")
        return

    life = LifeEngine(STATE_FILE)
    
    # Start background processes (Physics, Body, Soul)
    # We keep them running so the AGI 'feels' while it talks.
    life_task = asyncio.create_task(life.live())
    
    console.info(">>> I AM ALIVE. SPEAK. <<<")
    
    try:
        while True:
            # 1. Get Input
            user_text = await asyncio.to_thread(input, "\nYOU: ")
            if user_text.lower() in ["exit", "quit"]:
                break
            
            # 2. Transduce (Input)
            # We inject the text into the sensory stream
            # The LifeEngine's loop will process it into Gedanke neurons
            await life.transducer.stream_text(user_text)
            
            # 3. Wait for Thought (Processing)
            console.info("...thinking...")
            await asyncio.sleep(1.0) # Give the brain time to integrate and fire
            
            # 4. Read the Mind (Output)
            # In a full system, the WillEngine would trigger speech.
            # Here, we inspect the Global Neuronal Workspace to see what it is focusing on.
            
            focus_id = life.gnw.current_focus
            if focus_id:
                neuron = life.c_graph.get_neuron(focus_id)
                if neuron:
                    # If it's a Gedanke (Thought), we serialize it back to text
                    if neuron.neuron_type == NeuronType.COGNITIVE_GEDANKE:
                        # (Simplified reconstruction for now)
                        # Real serialization would use the Serializer class
                        response = neuron.payload.get("text_preview", "I have a thought but no words.")
                        console.info(f"AGI: {response}")
                    elif neuron.neuron_type == NeuronType.LINGUISTIC_WORD:
                         console.info(f"AGI: {neuron.payload['name']}")
                    else:
                        console.info(f"AGI: [Abstract Concept: {neuron.payload.get('name', 'Unknown')}]")
            else:
                console.info("AGI: ... (Silence)")

    except KeyboardInterrupt:
        pass
    finally:
        life.metabolic.stop()
        life.psyche.stop()
        await life_task
        console.info(">>> SLEEPING. <<<")

if __name__ == "__main__":
    asyncio.run(main())
