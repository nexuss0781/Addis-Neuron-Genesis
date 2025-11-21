import gzip
import json
import logging
import os
import tempfile
from uuid import UUID
from dataclasses import asdict
from enum import Enum

from .graph import NeuralGraph
from .resonance_graph import ResonanceGraph
from neuro_genome.schemas import Neuron, ResonanceNeuron
from neuro_genome.enums import NeuronType, SynapseType

logger = logging.getLogger(__name__)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, Enum):
            return obj.name
        return json.JSONEncoder.default(self, obj)

def hibernate_organism(conscious: NeuralGraph, subconscious: ResonanceGraph, filepath: str):
    """
    Saves the COMPLETE organism (Body, Mind, Soul) to a single file.
    Currently supports Conscious and Subconscious graphs.
    """
    temp_dir = os.path.dirname(os.path.abspath(filepath))
    temp_fd, temp_path = tempfile.mkstemp(dir=temp_dir)
    logger.info(f"Hibernation initiated. Saving to {filepath}")

    try:
        # Prepare Data Structure
        data = {
            "conscious": {str(k): asdict(v) for k, v in conscious._neurons.items()},
            "subconscious": {str(k): asdict(v) for k, v in subconscious._neurons.items()}
        }
        
        with os.fdopen(temp_fd, 'wb') as f_binary:
            with gzip.GzipFile(fileobj=f_binary, mode='wb') as f_gzip:
                json_string = json.dumps(data, cls=CustomJSONEncoder)
                f_gzip.write(json_string.encode('utf-8'))

        os.replace(temp_path, filepath)
        logger.info("Hibernation successful.")

    except Exception as e:
        logger.critical(f"Hibernation failed: {e}")
        os.remove(temp_path)
        raise

def reanimate_organism(filepath: str) -> tuple[NeuralGraph, ResonanceGraph]:
    """
    Loads the complete organism.
    """
    c_graph = NeuralGraph()
    r_graph = ResonanceGraph()
    
    if not os.path.exists(filepath):
        return c_graph, r_graph

    logger.info(f"Reanimation initiated from {filepath}")
    try:
        with gzip.open(filepath, 'rt', encoding='utf-8') as f:
            data = json.load(f)
            
        # Rehydrate Conscious
        for uid_str, n_data in data.get("conscious", {}).items():
            n_data['neuron_id'] = UUID(n_data['neuron_id'])
            n_data['neuron_type'] = NeuronType[n_data['neuron_type']]
            n_data['connections'] = [
                {**c, 'target_id': UUID(c['target_id']), 'type': SynapseType[c['type']]}
                for c in n_data['connections']
            ]
            # Handle symbolic vector if present
            # (Assuming it's a dict in the JSON, which matches schema)
            c_graph._neurons[n_data['neuron_id']] = Neuron(**n_data)

        # Rebuild Indexes
        for n in c_graph._neurons.values():
            c_graph._type_index[n.neuron_type].add(n.neuron_id)
            if 'name' in n.payload:
                c_graph._name_index[n.payload['name'].lower()] = n.neuron_id

        # Rehydrate Subconscious
        for uid_str, r_data in data.get("subconscious", {}).items():
            r_data['neuron_id'] = UUID(r_data['neuron_id'])
            # neuron_type is init=False, so we pop it if present or handle it manually
            if 'neuron_type' in r_data: del r_data['neuron_type']
            
            r_data['connections'] = [
                {**c, 'target_id': UUID(c['target_id'])}
                for c in r_data['connections']
            ]
            r_graph._neurons[r_data['neuron_id']] = ResonanceNeuron(**r_data)

        logger.info(f"Reanimation complete. C-Nodes: {len(c_graph)}, R-Nodes: {len(r_graph)}")
        return c_graph, r_graph

    except Exception as e:
        logger.critical(f"Reanimation failed: {e}")
        raise
