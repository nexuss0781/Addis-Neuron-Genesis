from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import List

@dataclass
class TraitLink:
    """
    A connection within a TraitComplex.
    """
    target_concept_name: str
    weight: float
    affective_charge: float # Positive (Virtue) or Negative (Vice) resonance

@dataclass
class TraitComplex:
    """
    A 'Memetic Virus' of personality.
    It is a template for a complex neural structure that can 'infect' the Psyche.
    """
    name: str # e.g., "CRUELTY", "ALTRUISM"
    
    # The Core Drive this trait satisfies (e.g., DOMINANCE for Cruelty)
    core_drive_axis: str 
    
    # The emotional fuel
    primary_emotion: str # e.g., "JOY", "ANGER"
    
    # The conceptual structure (The "Beliefs" of the trait)
    conceptual_links: List[TraitLink]
    
    # Properties of the Meme
    infectivity: float = 0.5 # How easily it is acquired (0.0 - 1.0)
    resilience: float = 0.5  # How hard it is to remove (0.0 - 1.0)
    
    trait_id: UUID = field(default_factory=uuid4)


# ======================================================================
# The Library of Human Nature
# ======================================================================

TRAIT_CRUELTY = TraitComplex(
    name="CRUELTY",
    core_drive_axis="Dominance",
    primary_emotion="JOY", # Schooled to find joy in dominance
    conceptual_links=[
        TraitLink("suffering", 0.8, 0.5),
        TraitLink("weakness", -0.5, -0.8),
        TraitLink("power", 1.0, 1.0)
    ],
    infectivity=0.7, 
    resilience=0.8
)

TRAIT_ALTRUISM = TraitComplex(
    name="ALTRUISM",
    core_drive_axis="Social",
    primary_emotion="JOY",
    conceptual_links=[
        TraitLink("help", 1.0, 1.0),
        TraitLink("self", -0.2, 0.0),
        TraitLink("pain", -1.0, -1.0)
    ],
    infectivity=0.3,
    resilience=0.6
)

TRAIT_CURIOSITY = TraitComplex(
    name="CURIOSITY",
    core_drive_axis="Arousal",
    primary_emotion="JOY",
    conceptual_links=[
        TraitLink("unknown", 1.0, 0.8),
        TraitLink("fear", -0.5, 0.0),
        TraitLink("learn", 1.0, 1.0)
    ],
    infectivity=0.9,
    resilience=0.5
)

ALL_TRAITS = [TRAIT_CRUELTY, TRAIT_ALTRUISM, TRAIT_CURIOSITY]
