import sqlite3
import logging
import json
from uuid import UUID
from enum import Enum

logger = logging.getLogger(__name__)

class AGIDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            logger.info(f"Database connection established to {self.db_path}")
        except sqlite3.Error as e:
            logger.critical(f"Database connection failed: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")

    def create_schema(self):
        if not self.conn:
            self.connect()

        cursor = self.conn.cursor()

        # Schema for Conscious Neurons
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conscious_neurons (
            neuron_id TEXT PRIMARY KEY,
            neuron_type TEXT NOT NULL,
            payload TEXT,
            symbolic_vector TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conscious_synapses (
            source_id TEXT NOT NULL,
            target_id TEXT NOT NULL,
            weight REAL NOT NULL,
            synapse_type TEXT NOT NULL,
            PRIMARY KEY (source_id, target_id),
            FOREIGN KEY (source_id) REFERENCES conscious_neurons (neuron_id),
            FOREIGN KEY (target_id) REFERENCES conscious_neurons (neuron_id)
        )
        """)

        # Schema for Subconscious Neurons
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subconscious_neurons (
            neuron_id TEXT PRIMARY KEY,
            payload TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subconscious_synapses (
            source_id TEXT NOT NULL,
            target_id TEXT NOT NULL,
            weight REAL NOT NULL,
            PRIMARY KEY (source_id, target_id),
            FOREIGN KEY (source_id) REFERENCES subconscious_neurons (neuron_id),
            FOREIGN KEY (target_id) REFERENCES subconscious_neurons (neuron_id)
        )
        """)

        self.conn.commit()
        logger.info("Database schema created or verified.")

    def save_graph(self, graph, graph_type: str):
        if not self.conn:
            self.connect()

        cursor = self.conn.cursor()

        if graph_type == 'conscious':
            # Clear old data
            cursor.execute("DELETE FROM conscious_synapses")
            cursor.execute("DELETE FROM conscious_neurons")

            # Save neurons
            for neuron in graph._neurons.values():
                cursor.execute(
                    "INSERT INTO conscious_neurons (neuron_id, neuron_type, payload, symbolic_vector) VALUES (?, ?, ?, ?)",
                    (
                        str(neuron.neuron_id),
                        neuron.neuron_type.name,
                        json.dumps(neuron.payload, cls=CustomJSONEncoder),
                        json.dumps(neuron.symbolic_vector, cls=CustomJSONEncoder) if neuron.symbolic_vector else None
                    )
                )
                # Save synapses
                for synapse in neuron.connections:
                    cursor.execute(
                        "INSERT OR IGNORE INTO conscious_synapses (source_id, target_id, weight, synapse_type) VALUES (?, ?, ?, ?)",
                        (str(neuron.neuron_id), str(synapse.target_id), synapse.weight, synapse.type.name)
                    )
        elif graph_type == 'subconscious':
            # Clear old data
            cursor.execute("DELETE FROM subconscious_synapses")
            cursor.execute("DELETE FROM subconscious_neurons")

            # Save neurons
            for neuron in graph._neurons.values():
                payload = {
                    'resonance_frequency': neuron.resonance_frequency,
                    'nap': neuron.nap,
                    'is_shadow': neuron.is_shadow,
                    'corruption_level': neuron.corruption_level
                }
                cursor.execute(
                    "INSERT INTO subconscious_neurons (neuron_id, payload) VALUES (?, ?)",
                    (
                        str(neuron.neuron_id),
                        json.dumps(payload, cls=CustomJSONEncoder)
                    )
                )
                # Save synapses
                for synapse in neuron.connections:
                    cursor.execute(
                        "INSERT OR IGNORE INTO subconscious_synapses (source_id, target_id, weight) VALUES (?, ?, ?)",
                        (str(neuron.neuron_id), str(synapse.target_id), synapse.weight)
                    )

        self.conn.commit()
        logger.info(f"Successfully saved {graph_type} graph to database.")

    def load_graph(self, graph, graph_type: str):
        if not self.conn:
            self.connect()

        from neuro_genome.schemas import Neuron, SynapticCleft, ResonanceNeuron
        from neuro_genome.enums import NeuronType, SynapseType

        cursor = self.conn.cursor()

        if graph_type == 'conscious':
            # Load neurons
            cursor.execute("SELECT neuron_id, neuron_type, payload, symbolic_vector FROM conscious_neurons")
            for row in cursor.fetchall():
                neuron_id, neuron_type, payload, symbolic_vector = row
                neuron = Neuron(
                    neuron_id=UUID(neuron_id),
                    neuron_type=NeuronType[neuron_type],
                    payload=json.loads(payload) if payload else {},
                    symbolic_vector=json.loads(symbolic_vector) if symbolic_vector else None
                )
                graph._neurons[neuron.neuron_id] = neuron

            # Load synapses
            cursor.execute("SELECT source_id, target_id, weight, synapse_type FROM conscious_synapses")
            for row in cursor.fetchall():
                source_id, target_id, weight, synapse_type = row
                synapse = SynapticCleft(
                    target_id=UUID(target_id),
                    weight=weight,
                    type=SynapseType[synapse_type]
                )
                graph._neurons[UUID(source_id)].connections.append(synapse)

        elif graph_type == 'subconscious':
            # Load neurons
            cursor.execute("SELECT neuron_id, payload FROM subconscious_neurons")
            for row in cursor.fetchall():
                neuron_id, payload = row
                neuron_data = json.loads(payload) if payload else {}
                neuron = ResonanceNeuron(
                    neuron_id=UUID(neuron_id),
                    resonance_frequency=neuron_data.get('resonance_frequency', 0.0),
                    nap=neuron_data.get('nap', 0.0),
                    is_shadow=neuron_data.get('is_shadow', False),
                    corruption_level=neuron_data.get('corruption_level', 0.0)
                )
                graph._neurons[neuron.neuron_id] = neuron

            # Load synapses
            cursor.execute("SELECT source_id, target_id, weight FROM subconscious_synapses")
            for row in cursor.fetchall():
                source_id, target_id, weight = row
                # Note: ResonanceNeuron synapse is a simple tuple in the original code
                # Let's assume it's a dict-like object for consistency
                synapse = {'target_id': UUID(target_id), 'weight': weight}
                graph._neurons[UUID(source_id)].connections.append(synapse)

        logger.info(f"Successfully loaded {graph_type} graph from database.")

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, Enum):
            return obj.name
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return super().default(obj)
