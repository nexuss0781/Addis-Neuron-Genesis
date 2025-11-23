from enum import Enum, auto

class NeuronType(Enum):
    """
    The formal classification of a Neuron's function, its "cell lineage."
    This dictates its payload and behavior within the Neuron Web.
    """
    # === SYSTEM 2: CONSCIOUS COGNITION ===
    # Linguistic Domain
    LINGUISTIC_ALPHABET = auto()
    LINGUISTIC_WORD = auto()
    LINGUISTIC_SENTENCE = auto() # Static Definition
    COGNITIVE_GEDANKE = auto()   # Dynamic Thought

    # Logical Domain
    LOGICAL_CONCEPT = auto()
    LOGICAL_RELATIONAL_OPERATOR = auto()
    LOGICAL_PATTERN = auto()
   

   # (Add these to NeuronType enum)
    LINGUISTIC_PARAGRAPH = auto()
    LINGUISTIC_PAGE = auto()
    LINGUISTIC_BOOK = auto()
    LINGUISTIC_SHELF = auto()
    LOGICAL_TOPIC = auto() # Replaces simple Topic

    # === SYSTEM 1: SUBCONSCIOUS PSYCHE ===
    # The fundamental particle of the subconscious
    RESONANCE_NODE = auto()

    # === SOMATIC & AFFECTIVE ===
    # Emotions and Vitals
    EMOTIONAL_PROTOTYPE = auto() # Legacy/Reference
    INTEROCEPTIVE_VITAL_SIGN = auto()
    INTEROCEPTIVE_DISEASE_SYMPTOM = auto()

    # === SENSORY & MOTOR ===
    SENSORY_TEXT_INPUT = auto()
    MOTOR_TEXT_OUTPUT = auto()

class SynapseType(Enum):
    """
    Defines the semantic meaning and function of a connection.
    """
    ASSOCIATIVE = auto()  # Bidirectional, Hebbian (Fire together, wire together)
    HIERARCHICAL = auto() # Parent -> Child (Structure)
    CAUSAL = auto()       # A -> B (Prediction)
    INHIBITORY = auto()   # A -> Suppress B (Competition)
    EXCITATORY = auto()   # A -> Boost B (Driver)
    SYMBOLIC = auto()     # Links a Concept to its Symbolic Vector
