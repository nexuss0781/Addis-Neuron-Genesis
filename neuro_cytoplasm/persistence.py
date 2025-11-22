import logging
import os
from .graph import NeuralGraph
from .resonance_graph import ResonanceGraph
from .db_storage import AGIDatabase

logger = logging.getLogger(__name__)

def hibernate_organism(conscious: NeuralGraph, subconscious: ResonanceGraph, filepath: str):
    """
    Saves the COMPLETE organism to a SQLite database.
    """
    db = AGIDatabase(db_path=filepath)
    try:
        db.connect()
        db.create_schema()
        db.save_graph(conscious, 'conscious')
        db.save_graph(subconscious, 'subconscious')
        logger.info(f"Hibernation successful. Organism saved to {filepath}")
    except Exception as e:
        logger.critical(f"Hibernation failed: {e}")
        raise
    finally:
        db.close()

def reanimate_organism(filepath: str) -> tuple[NeuralGraph, ResonanceGraph]:
    """
    Loads the complete organism from a SQLite database.
    """
    c_graph = NeuralGraph()
    r_graph = ResonanceGraph()
    
    if not os.path.exists(filepath):
        logger.warning(f"No database found at {filepath}. Returning empty graphs.")
        return c_graph, r_graph

    db = AGIDatabase(db_path=filepath)
    try:
        db.connect()
        db.load_graph(c_graph, 'conscious')
        db.load_graph(r_graph, 'subconscious')

        # Rebuild Indexes
        for n in c_graph._neurons.values():
            c_graph._type_index[n.neuron_type].add(n.neuron_id)
            if 'name' in n.payload:
                c_graph._name_index[n.payload['name'].lower()] = n.neuron_id

        logger.info(f"Reanimation complete from {filepath}. C-Nodes: {len(c_graph)}, R-Nodes: {len(r_graph)}")
        return c_graph, r_graph
    except Exception as e:
        logger.critical(f"Reanimation failed: {e}")
        raise
    finally:
        db.close()
