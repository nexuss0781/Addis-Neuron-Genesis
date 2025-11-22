import yaml
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def parse_and_validate_dictionary(filepath: str) -> List[Dict[str, Any]]:
    """
    Ingests, parses, and rigorously validates the Genesis Dictionary YAML file.
    This is the genetic transcription of the AGI's initial knowledge.
    """
    logger.info(f"Genetic Transcription initiated from {filepath}.")
    
    try:
        with open(filepath, 'r') as f:
            dictionary_data = yaml.safe_load(f)
    except FileNotFoundError:
        logger.critical(f"Genesis Dictionary not found at {filepath}. Aborting genesis.")
        raise
    except yaml.YAMLError as e:
        logger.critical(f"Failed to parse Genesis Dictionary: {e}. Aborting genesis.")
        raise

    if not isinstance(dictionary_data, list):
        raise ValueError("Genesis Dictionary must be a list of word entries.")

    # --- Relational Validation ---
    all_words = {entry['word'] for entry in dictionary_data if 'word' in entry}
    
    for i, entry in enumerate(dictionary_data):
        # Schema Validation
        if not all(k in entry for k in ['word', 'id', 'definitions']):
            raise ValueError(f"Entry #{i+1} ('{entry.get('word')}') is missing required keys.")

        # Synonym/Antonym Validation
        for rel_type in ['synonyms', 'antonyms']:
            if rel_type in entry:
                for related_word in entry[rel_type]:
                    if related_word not in all_words:
                        raise ValueError(
                            f"Broken link in entry '{entry['word']}': "
                            f"'{related_word}' in '{rel_type}' does not exist in the dictionary."
                        )
    
    logger.info(f"Genetic Transcription successful. {len(dictionary_data)} entries validated.")
    return dictionary_data
