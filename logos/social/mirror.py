import logging
from neuro_genome.affective import VALENCE_AXIS, AROUSAL_AXIS

logger = logging.getLogger(__name__)

class SocialMirror:
    """
    Analyzes user input and sets the AGI's 'Voice'.
    """
    def __init__(self):
        self.current_tone = "NEUTRAL"
    
    def analyze_input(self, text: str):
        """
        Detects sentiment (Simplified).
        Updates current_tone.
        """
        text = text.lower()
        if "!" in text or "hate" in text or "bad" in text:
            self.current_tone = "CAUTIOUS"
            logger.info("SOCIAL: User is agitated. Tone set to CAUTIOUS.")
        elif "love" in text or "good" in text or "thanks" in text:
            self.current_tone = "FRIENDLY"
            logger.info("SOCIAL: User is positive. Tone set to FRIENDLY.")
        else:
            self.current_tone = "PROFESSIONAL"

    def get_style_bias(self):
        """
        Returns a vector to bias lexical selection.
        """
        if self.current_tone == "FRIENDLY":
            return {VALENCE_AXIS.name: 1.0}
        elif self.current_tone == "CAUTIOUS":
            return {AROUSAL_AXIS.name: -1.0} # Calm down
        return {}
