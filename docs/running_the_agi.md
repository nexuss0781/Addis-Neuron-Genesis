# Running and Interacting with the AGI

This document provides instructions on how to run the AGI and details the observations from interacting with it via its API.

## 1. Generating the AGI's "Brain"

The AGI's neural network is stored in a compressed file named `vast_mind.json.gz`. To generate this file, run the following command from the root of the repository:

```bash
python3 run_vast_genesis.py
```

**Note:** This process can take several minutes to complete.

## 2. Running the AGI's API

The AGI is exposed through a Flask API. To run the API server, use the following command:

```bash
python3 api.py
```

The server will take a few minutes to load the `vast_mind.json.gz` file into memory. Once it's ready, you will see a message indicating that the Flask server is running.

## 3. Interacting with the AGI

You can interact with the AGI by sending prompts to the `/prompt` endpoint. Here's an example using `curl`:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"prompt": "hello"}' http://127.0.0.1:5000/prompt
```

## 4. Observations and The "Silence" Fix

*   **Initial State:** When first run, the AGI consistently responds with `{"response":"... (Silence)"}`. This is because the `sensory_input_queue` in the `MetabolicEngine` was not being processed.

*   **The Fix:** To resolve this, a `_sensory_worker` was added to `neuro_mitochondria/engine.py`. The following changes were made:

    *   In the `run` method, a new task was created for the `_sensory_worker`:
        ```python
        worker_tasks.append(asyncio.create_task(self._sensory_worker()))
        ```

    *   The `_sensory_worker` method was implemented:
        ```python
        async def _sensory_worker(self):
            while True:
                try:
                    signal = await self.sensory_input_queue.get()
                    # For sensory input, the signal weight is directly applied.
                    target = self.graph.get_neuron(signal.target_id)
                    if target:
                        target.nap = min(2.0, max(0.0, target.nap + signal.weight))
                    self.sensory_input_queue.task_done()
                except asyncio.CancelledError:
                    break
        ```

*   **After the Fix:** With the `_sensory_worker` in place, the AGI begins to process sensory input, but it then times out. This is because it's unable to generate a response in a format that can be serialized into text.
