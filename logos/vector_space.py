import math
import logging
from dataclasses import dataclass
from typing import List, Tuple

logger = logging.getLogger(__name__)

@dataclass
class Vector:
    """
    A high-dimensional vector representing a point in Semantic Space.
    Implemented in Pure Python for zero dependencies.
    """
    components: List[float]

    def __post_init__(self):
        if not self.components:
            self.components = [0.0] * 5 # Default 5D

    @property
    def dimensions(self) -> int:
        return len(self.components)

    def magnitude(self) -> float:
        """Calculates the Euclidean norm (length) of the vector."""
        return math.sqrt(sum(x**2 for x in self.components))

    def normalize(self) -> 'Vector':
        """Returns a unit vector in the same direction."""
        mag = self.magnitude()
        if mag == 0: return self
        return Vector([x / mag for x in self.components])

    def dot(self, other: 'Vector') -> float:
        """Calculates the dot product."""
        if self.dimensions != other.dimensions:
            # Graceful degradation for dimensionality mismatch (pad with 0)
            max_dim = max(self.dimensions, other.dimensions)
            a = self.components + [0.0] * (max_dim - self.dimensions)
            b = other.components + [0.0] * (max_dim - other.dimensions)
            return sum(x * y for x, y in zip(a, b))
        return sum(x * y for x, y in zip(self.components, other.components))

    def cosine_similarity(self, other: 'Vector') -> float:
        """
        The fundamental measure of semantic similarity.
        Range: -1.0 (Opposite) to 1.0 (Identical).
        """
        mag_a = self.magnitude()
        mag_b = other.magnitude()
        if mag_a == 0 or mag_b == 0:
            return 0.0
        return self.dot(other) / (mag_a * mag_b)

    def add(self, other: 'Vector') -> 'Vector':
        """Vector addition (Concept Blending)."""
        max_dim = max(self.dimensions, other.dimensions)
        a = self.components + [0.0] * (max_dim - self.dimensions)
        b = other.components + [0.0] * (max_dim - other.dimensions)
        return Vector([x + y for x, y in zip(a, b)])

    def subtract(self, other: 'Vector') -> 'Vector':
        """Vector subtraction (Concept Differentiation)."""
        max_dim = max(self.dimensions, other.dimensions)
        a = self.components + [0.0] * (max_dim - self.dimensions)
        b = other.components + [0.0] * (max_dim - other.dimensions)
        return Vector([x - y for x, y in zip(a, b)])
        
    def scale(self, scalar: float) -> 'Vector':
        """Scalar multiplication."""
        return Vector([x * scalar for x in self.components])

    def __repr__(self):
        return f"Vector({[round(c, 3) for c in self.components]})"


class SemanticSpace:
    """
    Manages the coordinate system of the AGI's mind.
    """
    def __init__(self):
        self.vectors: List[Tuple[str, Vector]] = [] # (ID, Vector)
        logger.info("SemanticSpace initialized.")

    def register_point(self, id_tag: str, vector: Vector):
        """Adds a concept to the space."""
        self.vectors.append((id_tag, vector))

    def find_nearest(self, target: Vector, n: int = 1) -> List[Tuple[str, float]]:
        """
        Finds the 'n' closest concepts to the target vector.
        Returns list of (ID, similarity_score).
        """
        scores = []
        for id_tag, vec in self.vectors:
            sim = target.cosine_similarity(vec)
            scores.append((id_tag, sim))
        
        # Sort by similarity descending
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:n]

    def get_centroid(self, vectors: List[Vector]) -> Vector:
        """Calculates the average (center) of a group of vectors."""
        if not vectors: return Vector([])
        
        sum_vec = vectors[0]
        for i in range(1, len(vectors)):
            sum_vec = sum_vec.add(vectors[i])
            
        return sum_vec.scale(1.0 / len(vectors))
