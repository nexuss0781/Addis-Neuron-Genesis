
import asyncio
import threading
from flask import Flask, request, jsonify
from life.engine import LifeEngine
from neuro_genome.enums import NeuronType
import os
import sys
import time

# Path setup
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

app = Flask(__name__)

STATE_FILE = "vast_mind.json.gz"
life = None
agi_loop = None
agi_thread = None

def agi_event_loop(loop):
    """The function that will run in the background thread."""
    asyncio.set_event_loop(loop)
    loop.run_forever()

def initialize_agi():
    """Initializes and starts the AGI in a background thread."""
    global life, agi_loop, agi_thread

    if life is not None:
        return # Already initialized

    if not os.path.exists(STATE_FILE):
        raise FileNotFoundError(f"Brain file {STATE_FILE} not found! Run run_vast_genesis.py first.")

    # Create and start the event loop in a separate thread
    agi_loop = asyncio.new_event_loop()
    agi_thread = threading.Thread(target=agi_event_loop, args=(agi_loop,), daemon=True)
    agi_thread.start()

    # Define the coroutine to run in the event loop
    async def main():
        global life
        life = LifeEngine(STATE_FILE)
        await life.live()

    # Schedule the main coroutine to run in the background event loop
    asyncio.run_coroutine_threadsafe(main(), agi_loop)

@app.route('/prompt', methods=['POST'])
def prompt():
    if life is None or agi_loop is None:
        return jsonify({"error": "AGI not initialized or still loading."}), 503

    data = request.get_json()
    user_text = data.get('prompt')

    if not user_text:
        return jsonify({"error": "Prompt is missing"}), 400

    # This coroutine will be executed in the AGI's event loop
    async def do_prompt():
        await life.transducer.stream_text(user_text)
        await asyncio.sleep(1.0) # Give time for processing

        focus_id = life.gnw.current_focus
        if focus_id:
            neuron = life.c_graph.get_neuron(focus_id)
            if neuron:
                if neuron.neuron_type == NeuronType.COGNITIVE_GEDANKE:
                    response = neuron.payload.get("text_preview", "I have a thought but no words.")
                elif neuron.neuron_type == NeuronType.LINGUISTIC_WORD:
                    response = neuron.payload['name']
                else:
                    response = f"[Abstract Concept: {neuron.payload.get('name', 'Unknown')}]"
                return response
        return "... (Silence)"

    # Schedule the coroutine and wait for the result
    future = asyncio.run_coroutine_threadsafe(do_prompt(), agi_loop)
    try:
        # Wait for the result with a timeout
        result = future.result(timeout=10)
        return jsonify({"response": result})
    except asyncio.TimeoutError:
        return jsonify({"error": "AGI took too long to respond."}), 504
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500


if __name__ == '__main__':
    print("Initializing AGI...")
    initialize_agi()
    # It takes a long time to load the brain, so we need to wait before starting the server.
    # A better approach would be a readiness probe.
    print("Waiting for AGI to load... This may take several minutes.")
    while life is None:
        time.sleep(1)
    print("AGI loaded. Starting Flask server.")
    app.run(host='0.0.0.0', port=5000)
