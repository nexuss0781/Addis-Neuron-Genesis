# AGI Memory System: Database Implementation

## 1. Overview

This document details the implementation of the new database-backed memory system for the AGI. The previous `json.gz` file-based storage has been replaced with a SQLite database to provide a more robust, scalable, and dynamic solution for persisting the AGI's neural state.

The new architecture is designed to seamlessly integrate with the existing codebase while offering significant improvements in performance and data management.

## 2. Architecture

The database implementation is centered around three key components:

- **Database Core (`db_storage.py`):** A dedicated module to manage all database operations, including connection, schema creation, and data persistence.
- **Persistence Layer (`persistence.py`):** The existing persistence layer has been adapted to act as an intermediary between the AGI's neural graphs and the database core.
- **High-Level Scripts (`gestate.py`, `live.py`):** These scripts have been updated to use the new `.db` file extension, ensuring a smooth transition to the new storage system.

## 3. Database Schema

The SQLite database is structured to accurately model the AGI's conscious and subconscious neural networks. The schema is defined as follows:

### Conscious Network

- **`conscious_neurons`**
  - `neuron_id` (TEXT, PRIMARY KEY): The unique identifier for the neuron.
  - `neuron_type` (TEXT): The type of the neuron (e.g., `LINGUISTIC_WORD`, `COGNITIVE_GEDANKE`).
  - `payload` (TEXT): A JSON object containing neuron-specific data.
  - `symbolic_vector` (TEXT): A JSON object representing the neuron's symbolic vector.

- **`conscious_synapses`**
  - `source_id` (TEXT): The ID of the source neuron.
  - `target_id` (TEXT): The ID of the target neuron.
  - `weight` (REAL): The strength of the synaptic connection.
  - `synapse_type` (TEXT): The type of synapse (e.g., `ASSOCIATIVE`, `HIERARCHICAL`).

### Subconscious Network

- **`subconscious_neurons`**
  - `neuron_id` (TEXT, PRIMARY KEY): The unique identifier for the neuron.
  - `payload` (TEXT): A JSON object containing neuron-specific data.

- **`subconscious_synapses`**
  - `source_id` (TEXT): The ID of the source neuron.
  - `target_id` (TEXT): The ID of the target neuron.
  - `weight` (REAL): The strength of the synaptic connection.

## 4. Implementation Details

### `db_storage.py`

The `AGIDatabase` class in `db_storage.py` is the cornerstone of the new memory system. It provides the following key methods:

- `connect()`: Establishes a connection to the SQLite database.
- `create_schema()`: Creates the necessary tables if they do not already exist.
- `save_graph()`: Serializes and saves a neural graph (conscious or subconscious) to the database.
- `load_graph()`: Deserializes and loads a neural graph from the database.

### `persistence.py`

The `hibernate_organism` and `reanimate_organism` functions have been refactored to delegate all storage and retrieval operations to the `AGIDatabase` class. This approach maintains a clean separation of concerns and minimizes the impact on the surrounding codebase.

## 5. Rationale

The decision to migrate to a SQLite database was driven by several factors:

- **Scalability:** SQLite can handle large datasets with ease, providing a solid foundation for the AGI's future growth.
- **Dynamic Data Management:** The database allows for more flexible and efficient data manipulation, paving the way for more advanced memory operations.
- **Robustness:** SQLite is a well-tested and reliable database engine, ensuring the integrity of the AGI's memory.
- **Performance:** For the current scale of the AGI, SQLite offers excellent performance with low overhead.

## 6. Conclusion

The new database-backed memory system represents a significant step forward in the AGI's development. It provides a more powerful and flexible foundation for memory management, and it is designed to support the AGI's continued evolution.
