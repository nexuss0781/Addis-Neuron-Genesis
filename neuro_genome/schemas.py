from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import List, Dict, Any, Optional

from .enums import NeuronType, SynapseType

@dataclass
class SynapticCleft:
    """
    The physical connection in the Conscious Mind.
    """
    target_id: UUID
    weight: float
    type: SynapseType
    # Phase shift for wave mechanics (bridging to subconscious physics)
    phase_shift: float = 0.0

@dataclass
class Neuron:
    """
    The fundamental particle of the Conscious Mind (System 2).
    Holds Data, State, and Logic.
    """
    neuron_id: UUID = field(default_factory=uuid4)
    neuron_type: NeuronType = NeuronType.LOGICAL_CONCEPT
    
    # Dynamic State
    nap: float = 0.0               # Activation Potential
    activation_count: int = 0      # Usage Metric
    last_fired_tick: int = -1      # Refractory Timer
    
    # Knowledge
    connections: List[SynapticCleft] = field(default_factory=list)
    payload: Dict[str, Any] = field(default_factory=dict)
    
    # Reinforcement Learning State
    expected_value: float = 0.0    # Dopaminergic Value
    value_confidence: float = 0.0  # Certainty
    
    # Symbolic State (5D Meaning Space)
    # Stored as dict for serialization: {'order': 0.5, 'chaos': -0.5 ...}
    symbolic_vector: Optional[Dict[str, float]] = None

@dataclass
class ResonanceCleft:
    """
    The connection in the Subconscious Mind.
    Purely physics-based.
    """
    target_id: UUID
    weight: float
    phase_shift: float

@dataclass
class ResonanceNeuron:
    """
    The fundamental particle of the Subconscious Mind (System 1).
    Holds Frequency and Energy. No Data.
    """
    neuron_id: UUID = field(default_factory=uuid4)
    neuron_type: NeuronType = field(default=NeuronType.RESONANCE_NODE, init=False)
    
    # Intrinsic Physics
    resonance_frequency: float = field(default_factory=float)
    
    # Dynamic State
    nap: float = 0.0 # Current Energy Level
    
    # Wiring
    connections: List[ResonanceCleft] = field(default_factory=list)
    
    # Shadow State
    is_shadow: bool = False
    corruption_level: float = 0.0
