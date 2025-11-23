import logging
from dataclasses import dataclass, field
from typing import List, Optional, Dict

logger = logging.getLogger(__name__)

@dataclass
class Morpheme:
    """
    The smallest unit of meaning.
    """
    text: str
    type: str # 'ROOT', 'PREFIX', 'SUFFIX'
    meaning_vector: List[float] = field(default_factory=list)

class EtymologyEngine:
    """
    The Root System. Handles Deconstruction and Synthesis of words.
    """
    def __init__(self):
        self.roots: Dict[str, Morpheme] = {}
        self.prefixes: Dict[str, Morpheme] = {}
        self.suffixes: Dict[str, Morpheme] = {}
        self._seed_morphemes()
        logger.info("EtymologyEngine initialized.")

    def _seed_morphemes(self):
        # Seed with basic English/Latin/Greek roots
        # In a full system, this would be loaded from a genome file
        self.prefixes['un'] = Morpheme('un', 'PREFIX', [-1.0, 0.0, 0.0, 0.0, 0.0]) # Negation
        self.prefixes['re'] = Morpheme('re', 'PREFIX', [0.0, 0.0, 0.0, 0.0, 0.5]) # Repetition
        self.prefixes['bio'] = Morpheme('bio', 'PREFIX', [0.8, 0.0, 0.0, 0.0, 0.0]) # Life
        
        self.suffixes['logy'] = Morpheme('logy', 'SUFFIX', [0.0, 1.0, 0.0, 0.0, 0.0]) # Study of
        self.suffixes['ist'] = Morpheme('ist', 'SUFFIX', [0.0, 0.0, 1.0, 0.0, 0.0]) # Person
        
        self.roots['graph'] = Morpheme('graph', 'ROOT')
        self.roots['struct'] = Morpheme('struct', 'ROOT')

    def deconstruct(self, word: str) -> List[Morpheme]:
        """
        Attempts to break an unknown word into known morphemes.
        Returns a list of Morpheme objects if successful.
        """
        word = word.lower()
        components = []
        
        # 1. Check Prefixes
        for p_str, m in self.prefixes.items():
            if word.startswith(p_str):
                components.append(m)
                word = word[len(p_str):] # Strip prefix
                break # Assume one prefix for simplicity
        
        # 2. Check Suffixes
        for s_str, m in self.suffixes.items():
            if word.endswith(s_str):
                # Store suffix to append later (order matters)
                # We need to find the root first
                remaining = word[:-len(s_str)]
                # Check if remaining is a known root
                # (Simplified check)
                root = Morpheme(remaining, 'ROOT') 
                components.append(root)
                components.append(m)
                return components
                
        # If no suffix match, what's left is the root
        if word:
            components.append(Morpheme(word, 'ROOT'))
            
        return components

    def synthesize(self, root: str, prefix: str = None, suffix: str = None) -> str:
        """
        Combines components to invent a new word string.
        e.g., synthesize('construct', 're', 'ion') -> 'reconstruction'
        """
        word = root
        if prefix:
            word = prefix + word
        if suffix:
            # Basic English morphology rule (e.g., dropping 'e') could go here
            word = word + suffix
        return word
