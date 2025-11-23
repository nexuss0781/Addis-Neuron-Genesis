import logging
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

@dataclass
class SensoryProfile:
    """
    A 5-channel vector representing the sensory experience of a concept.
    Values range 0.0 (None) to 1.0 (Intense).
    """
    visual: float = 0.0      # Brightness / Color intensity
    auditory: float = 0.0    # Loudness / Pitch
    tactile: float = 0.0     # Texture / Temperature / Pain
    olfactory: float = 0.0   # Smell
    gustatory: float = 0.0   # Taste
    
    # Dominant descriptive tags (e.g., "Red", "Loud", "Sweet")
    tags: List[str] = field(default_factory=list)

class SynesthesiaMap:
    """
    Maps abstract concepts to concrete sensory profiles.
    This is the 'Mind's Eye' and 'Mind's Ear'.
    """
    def __init__(self):
        self.profiles: Dict[str, SensoryProfile] = {}
        self._seed_senses()
        logger.info("SynesthesiaMap initialized. Sensory channels open.")

    def _seed_senses(self):
        # In a full system, these would be learned from adjectives in the text.
        # For Genesis, we seed the archetypes.
        
        self.profiles["fire"] = SensoryProfile(visual=0.9, tactile=1.0, tags=["Red", "Hot", "Pain"])
        self.profiles["ice"] = SensoryProfile(visual=0.7, tactile=0.9, tags=["White", "Cold", "Numb"])
        self.profiles["thunder"] = SensoryProfile(auditory=1.0, tactile=0.3, tags=["Loud", "Rumble", "Vibration"])
        self.profiles["honey"] = SensoryProfile(visual=0.6, tactile=0.8, gustatory=1.0, tags=["Gold", "Sticky", "Sweet"])
        self.profiles["void"] = SensoryProfile(visual=0.1, auditory=0.1, tactile=0.0, tags=["Dark", "Silent", "Cold"])

    def get_profile(self, concept_name: str) -> SensoryProfile:
        """Retrieves the sensory profile for a concept. Returns default if not found."""
        return self.profiles.get(concept_name.lower(), SensoryProfile())

    def ground_concept(self, concept_name: str, profile: SensoryProfile):
        """Learns a new sensory association."""
        self.profiles[concept_name.lower()] = profile
        logger.debug(f"SENSORY: Concept '{concept_name}' grounded with profile {profile.tags}.")

    def hallucinate(self, text_stream: List[str]) -> SensoryProfile:
        """
        Takes a stream of words and generates the aggregate sensory experience.
        This is the AGI 'imagining' the scene.
        """
        total_experience = SensoryProfile()
        count = 0
        
        for word in text_stream:
            profile = self.get_profile(word)
            # Add up the sensory intensities
            total_experience.visual += profile.visual
            total_experience.auditory += profile.auditory
            total_experience.tactile += profile.tactile
            total_experience.olfactory += profile.olfactory
            total_experience.gustatory += profile.gustatory
            total_experience.tags.extend(profile.tags)
            
            if any([profile.visual, profile.auditory, profile.tactile, profile.olfactory, profile.gustatory]):
                count += 1
        
        # Normalize (Average experience)
        if count > 0:
            total_experience.visual /= count
            total_experience.auditory /= count
            total_experience.tactile /= count
            total_experience.olfactory /= count
            total_experience.gustatory /= count
            
        return total_experience
