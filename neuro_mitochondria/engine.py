import asyncio
import logging
import os
import collections
from dataclasses import dataclass
from uuid import UUID
from typing import Deque, Optional

from genesis import config
from neuro_cytoplasm.graph import NeuralGraph
# Use forward reference or 'Any' to avoid circular import with PsycheEngine during definition
from typing import Any 

logger = logging.getLogger(__name__)

@dataclass
class Signal:
    source_id: UUID
    target_id: UUID
    weight: float

class MetabolicEngine:
    """
    The Asynchronous CPU. Drives the Universal Clock and Signal Propagation.
    """
    def __init__(self, graph: NeuralGraph, psyche_engine: Any, tick_duration: float = 0.01):
        self.graph = graph
        self.psyche_engine = psyche_engine
        self.tick_duration = tick_duration
        self.current_tick: int = 0
        self.is_running: bool = False
        
        # Queues
        self.signal_queue: asyncio.Queue[Signal] = asyncio.Queue()
        self.sensory_input_queue: asyncio.Queue[Signal] = asyncio.Queue()
        self.intuition_queue: asyncio.Queue[Any] = asyncio.Queue() # Accepts IntuitiveBias
        
        # Memory
        self.firing_trace: Deque = collections.deque(maxlen=100)

        # Consciousness Interface
        self.gnw = None
        
        logger.info("MetabolicEngine (The CPU) initialized.")

    async def run(self):
        if self.is_running: return
        self.is_running = True
        logger.warning("MetabolicEngine started.")
        
        # Start Workers
        worker_tasks = [
            asyncio.create_task(self._signal_worker())
            for _ in range(os.cpu_count() or 1)
        ]

        try:
            while self.is_running:
                self.current_tick += 1
                
                # 1. Physics Cycle
                await self.signal_queue.join() # Wait for signals to process
                await self._check_for_firings()
                await self._apply_decay()

                # 2. Consciousness Cycle
                if self.gnw:
                    self.gnw.update_focus()
                
                # 3. Tick
                await asyncio.sleep(self.tick_duration)
        finally:
            self.is_running = False
            for t in worker_tasks: t.cancel()

    def stop(self):
        self.is_running = False

    async def _signal_worker(self):
        while True:
            try:
                signal = await self.signal_queue.get()
                target = self.graph.get_neuron(signal.target_id)
                if target:
                    target.nap = min(2.0, max(0.0, target.nap + signal.weight))
                self.signal_queue.task_done()
            except asyncio.CancelledError:
                break

    async def _check_for_firings(self):
        # Simple scan for Phase 2.0
        for neuron in self.graph._neurons.values():
            if (self.current_tick - neuron.last_fired_tick) < config.REFRACTORY_PERIOD_TICKS:
                continue
            
            if neuron.nap >= 1.0:
                # Fire!
                neuron.nap = 0.0
                neuron.last_fired_tick = self.current_tick
                neuron.activation_count += 1
                self.firing_trace.append((self.current_tick, neuron.neuron_id))
                
                # Notify Subconscious
                if self.psyche_engine:
                    self.psyche_engine.receive_ping(neuron.neuron_id, self.current_tick)
                
                # Propagate
                for cleft in neuron.connections:
                    self.signal_queue.put_nowait(
                        Signal(neuron.neuron_id, cleft.target_id, cleft.weight)
                    )

    async def _apply_decay(self):
        for neuron in self.graph._neurons.values():
            if 0.0 < neuron.nap < 1.0:
                neuron.nap = max(0.0, neuron.nap * (1 - config.DECAY_RATE))
