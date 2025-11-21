from dataclasses import dataclass
from genesis_trinity.health.soma_graph import OrganType 
# Wait, SomaGraph isn't defined yet in this order. 
# I will use string literals for organ names in the Genome to decouple.

@dataclass(frozen=True)
class DriveAxis:
    name: str
    linked_organ_name: str
    base_frequency: float
    urgency_multiplier: float

DRIVE_ENERGY = DriveAxis("Energy Drive", "BATTERY", 20.0, 3.0)
DRIVE_INTEGRITY = DriveAxis("Integrity Drive", "INTEGRITY", 25.0, 5.0)
DRIVE_GROWTH = DriveAxis("Growth Drive", "PLASTICITY", 30.0, 1.5)

ALL_DRIVES = [DRIVE_ENERGY, DRIVE_INTEGRITY, DRIVE_GROWTH]
