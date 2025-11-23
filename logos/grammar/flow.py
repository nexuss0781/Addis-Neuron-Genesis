import logging
from typing import List, Tuple, Dict
from enum import Enum, auto

logger = logging.getLogger(__name__)

# Simplified POS tags for the physics engine
class SyntaxTag(Enum):
    NOUN = auto()
    VERB = auto()
    ADJ = auto()
    ADV = auto()
    DET = auto() # Determiner (The, A)
    PREP = auto()
    END = auto() # Sentence end

class SyntacticFlow:
    """
    Calculates the 'Potential Energy' of a sentence structure.
    Language flows from High Potential (Unresolved) to Low Potential (Resolved).
    """
    def __init__(self):
        # Valency Map: What does each tag 'want'?
        # Key: Source Tag. Value: List of (Target Tag, Energy Change)
        # Negative Energy Change = Release/Stability (Good)
        # Positive Energy Change = Friction/Instability (Bad)
        self.valency_map: Dict[SyntaxTag, List[Tuple[SyntaxTag, float]]] = {
            SyntaxTag.DET:  [(SyntaxTag.NOUN, -1.0), (SyntaxTag.ADJ, -0.5)],
            SyntaxTag.ADJ:  [(SyntaxTag.NOUN, -1.0)],
            SyntaxTag.NOUN: [(SyntaxTag.VERB, -1.0), (SyntaxTag.PREP, -0.5), (SyntaxTag.END, -1.0)],
            SyntaxTag.VERB: [(SyntaxTag.NOUN, -1.0), (SyntaxTag.ADV, -0.5), (SyntaxTag.PREP, -0.5), (SyntaxTag.END, -1.0)],
            SyntaxTag.PREP: [(SyntaxTag.NOUN, -1.0), (SyntaxTag.DET, -0.5)],
            SyntaxTag.ADV:  [(SyntaxTag.VERB, -0.5), (SyntaxTag.ADJ, -0.5)]
        }
        logger.info("SyntacticFlow physics initialized.")

    def analyze_flow(self, sequence: List[SyntaxTag]) -> float:
        """
        Returns the Total Energy of the sequence.
        Lower energy = Better grammar.
        """
        total_energy = 0.0
        current_potential = 1.0 # Starting tension
        
        for i in range(len(sequence) - 1):
            source = sequence[i]
            target = sequence[i+1]
            
            # Find interaction
            interaction = self._get_interaction(source, target)
            
            if interaction:
                # Valid grammatical move. Energy is released.
                delta = interaction
                current_potential += delta
                # Energy cannot drop below zero until the end
                current_potential = max(0.1, current_potential)
            else:
                # Invalid move. Friction spikes.
                logger.debug(f"SYNTAX CLASH: {source.name} -> {target.name}")
                total_energy += 1.0 # Penalty
                current_potential += 0.5 # Tension rises
        
        # Final check: Is the sentence resolved?
        if current_potential > 0.2:
            total_energy += current_potential # Unresolved tension penalty
            
        return total_energy

    def _get_interaction(self, source: SyntaxTag, target: SyntaxTag) -> float | None:
        """Look up valency."""
        options = self.valency_map.get(source, [])
        for valid_target, energy_delta in options:
            if valid_target == target:
                return energy_delta
        return None
