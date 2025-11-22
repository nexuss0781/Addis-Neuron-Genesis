from dataclasses import dataclass

@dataclass(frozen=True)
class PrimalAxis:
    name: str
    positive_pole_name: str
    negative_pole_name: str
    base_frequency: float

# The Pleasure <-> Displeasure Axis
VALENCE_AXIS = PrimalAxis("Valence", "Pleasure", "Displeasure", 3.14159)
# The Activation <-> Passivity Axis
AROUSAL_AXIS = PrimalAxis("Arousal", "Activation", "Passivity", 6.28318)
# The Control <-> Submissiveness Axis
DOMINANCE_AXIS = PrimalAxis("Dominance", "Control", "Submissiveness", 9.42477)

ALL_PRIMAL_AXES = [VALENCE_AXIS, AROUSAL_AXIS, DOMINANCE_AXIS]
