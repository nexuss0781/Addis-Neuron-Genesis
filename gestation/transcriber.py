import yaml
import logging
from typing import List, Dict, Any

from neuro_genome.symbolic import VECTOR_SEEDS

logger = logging.getLogger(__name__)

class GeneticTranscriber:
    """
    Parses the Genesis Dictionary and injects Genetic Constants (Symbolic Vectors).
    """
    def parse(self, filepath: str) -> List[Dict[str, Any]]:
        logger.info(f"Transcribing genome from {filepath}...")
        try:
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            logger.critical(f"Genetic Transcription failed: {e}")
            raise

        # Validation & Injection Pass
        all_words = {entry['word'] for entry in data}
        
        for entry in data:
            word = entry['word']
            # 1. Validate Links
            for rel in ['synonyms', 'antonyms']:
                for link in entry.get(rel, []):
                    if link not in all_words:
                        raise ValueError(f"Broken genetic link: {word} -> {link}")
            
            # 2. Inject Symbolic Seed
            if word in VECTOR_SEEDS:
                # Convert the Vector object to a dict for the Neuron payload
                entry['symbolic_seed'] = VECTOR_SEEDS[word].to_dict()
                logger.debug(f"Injected Symbolic Seed for '{word}'.")

        logger.info(f"Transcription complete. {len(data)} genes validated.")
        return data
