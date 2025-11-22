from dataclasses import dataclass

@dataclass(frozen=True)
class DriveAxis:
    name: str
    linked_organ_name: str
    base_frequency: float
    urgency_multiplier: float

# The Innate Drives
# Note: linked_organ_name must match the OrganType enum names in soma/graph.py

DRIVE_ENERGY = DriveAxis(
    name="Energy Drive", 
    linked_organ_name="BATTERY", 
    base_frequency=20.0, 
    urgency_multiplier=3.0
)

DRIVE_INTEGRITY = DriveAxis(
    name="Integrity Drive", 
    linked_organ_name="INTEGRITY", 
    base_frequency=25.0, 
    urgency_multiplier=5.0
)

DRIVE_GROWTH = DriveAxis(
    name="Growth Drive", 
    linked_organ_name="PLASTICITY", 
    base_frequency=30.0, 
    urgency_multiplier=1.5
)

ALL_DRIVES = [DRIVE_ENERGY, DRIVE_INTEGRITY, DRIVE_GROWTH]
