
    import asyncio
    import logging

    from genesis_trinity import config
    from neuro_cytoplasm.graph import NeuralGraph
    from neuro_mitochondria.engine import MetabolicEngine, Signal
    from neuro_genome.enums import NeuronType

    logger = logging.getLogger(__name__)

    class LexicalTransducer:
        """
        The AGI's "Optic Nerve."

        This engine's sole responsibility is to convert a raw text string into
        a timed stream of Signal events and place them onto the dedicated
        SENSORY INPUT queue.
        """
        def __init__(self, graph: NeuralGraph, engine: MetabolicEngine):
            self.graph = graph
            self.engine = engine
            self._alphabet_cache = {
                n.payload['character']: n.neuron_id
                for n in self.graph.get_neurons_by_type(NeuronType.LINGUISTIC_ALPHABET)
            }
            logger.info(f"LexicalTransducer (Optic Nerve) initialized with {len(self._alphabet_cache)} characters.")

        async def stream_text(self, text: str):
            """
            Takes a string and streams it into the SENSORY_INPUT_QUEUE.
            """
            logger.debug(f"Streaming text into sensory pathway: '{text[:50]}...'
")

            for char in text:
                char_lower = char.lower()
                char_neuron_id = self._alphabet_cache.get(char_lower)

                if char_neuron_id:
                    signal = Signal(
                        source_id=char_neuron_id,
                        target_id=char_neuron_id,
                        weight=1.0
                    )
                    # Puts the signal on the DEDICATED sensory queue
                    await self.engine.sensory_input_queue.put(signal)
                else:
                    # logger.warning(f"Character '{char}' not in Canonical Alphabet. Skipping.")
                    pass

                await asyncio.sleep(config.TICK_DURATION)
