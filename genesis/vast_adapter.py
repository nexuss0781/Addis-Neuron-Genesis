import json
import logging
import re
from typing import List, Dict, Any, Generator

logger = logging.getLogger(__name__)

# Heuristic map for Part-of-Speech normalization
POS_MAP = {
    "n.": "NOUN",
    "v.": "VERB", 
    "v. t.": "VERB",
    "v. i.": "VERB",
    "adj.": "ADJECTIVE",
    "adv.": "ADVERB",
    "prep.": "PREPOSITION",
    "conj.": "CONJUNCTION",
    "pron.": "PRONOUN",
    "interj.": "INTERJECTION",
    "art.": "ARTICLE"
}

class VastDictionaryAdapter:
    """
    Ingests a raw, large-scale dictionary JSON and adapts it to the
    Genesis Trinity genetic schema. Handles streaming to manage memory.
    """
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.valid_entries = 0
        self.skipped_entries = 0

    def stream_entries(self) -> Generator[Dict[str, Any], None, None]:
        """
        Yields cleaned, validated dictionary entries one by one.
        """
        logger.info(f"Opening vast dictionary at {self.filepath}...")
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                # We assume the JSON is a list of objects.
                # For truly massive files (GBs), we'd use a streaming library like ijson.
                # For standard dictionaries (MBs), json.load is fine.
                raw_data = json.load(f)
                
            logger.info(f"JSON loaded. Processing {len(raw_data)} raw entries...")

            for raw_entry in raw_data:
                cleaned_entry = self._normalize_entry(raw_entry)
                if cleaned_entry:
                    self.valid_entries += 1
                    yield cleaned_entry
                else:
                    self.skipped_entries += 1
            
            logger.info(f"Adaptation complete. {self.valid_entries} valid, {self.skipped_entries} skipped.")

        except Exception as e:
            logger.critical(f"Failed to adapt dictionary: {e}")
            raise

    def _normalize_entry(self, raw: Dict) -> Dict | None:
        """
        Transforms a single raw entry into the Genesis schema.
        """
        word = raw.get("word")
        if not word: return None
        
        # 1. Normalize POS
        raw_pos = raw.get("pos", "").lower().strip()
        # Try exact match first, then partial
        pos_tag = POS_MAP.get(raw_pos, "CONCEPT") # Default to generic Concept
        if pos_tag == "CONCEPT":
            # Fuzzy match: if it starts with "n.", it's a noun
            for k, v in POS_MAP.items():
                if raw_pos.startswith(k):
                    pos_tag = v
                    break
        
        # 2. Normalize Definitions
        definitions = []
        raw_defs = raw.get("definitions", [])
        for d_text in raw_defs:
            if not d_text: continue
            # Basic cleaning
            d_text = d_text.strip()
            definitions.append({
                "pos": pos_tag,
                "text": d_text
            })
            
        if not definitions: return None

        # 3. Extract Synonyms (This is tricky with free text)
        synonyms = []
        raw_syns = raw.get("synonyms", "")
        if raw_syns:
            # Remove "See", "Notes", parentheses
            # Regex to find words: split by comma or semicolon
            clean_syns = re.split(r'[,;]', raw_syns)
            for s in clean_syns:
                s = s.strip()
                # Filter out junk (e.g., "See also")
                if s and " " not in s and s.lower() != word.lower():
                     synonyms.append(s.lower())

        # 4. Construct ID
        # Use a sanitized version of the word for the ID
        clean_word_id = re.sub(r'\W+', '', word).lower()
        lexical_id = f"en_{clean_word_id}_auto"

        return {
            "word": word.lower(), # Store lowercase for consistency
            "id": lexical_id,
            "language": "en",
            "definitions": definitions,
            "synonyms": synonyms,
            "antonyms": [] # Raw JSON usually doesn't have explicit antonyms structure
        }
