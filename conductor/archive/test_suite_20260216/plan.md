# Plan: Establishment of Test Suite and Core Utility Coverage

## Phase 1: Test Infrastructure Setup [checkpoint: 57a0929]
- [x] Task: Configure pytest and coverage in `pyproject.toml` or `pytest.ini` 6896277
- [x] Task: Create initial test directory structure and `conftest.py` with necessary fixtures 6f06d88
- [x] Task: Conductor - User Manual Verification 'Phase 1: Test Infrastructure Setup' (Protocol in workflow.md)

## Phase 2: Unit Tests for db_handler.py [checkpoint: 72d9cab]
- [x] Task: Write unit tests for `db_handler.py` covering `init_nodedb` and `save_message_to_db` 6165e66
- [x] Task: Write unit tests for `db_handler.py` covering node info updates and name retrieval abde011
- [x] Task: Conductor - User Manual Verification 'Phase 2: Unit Tests for db_handler.py' (Protocol in workflow.md)

## Phase 3: Unit Tests for utils.py [checkpoint: ab27e4f]
- [x] Task: Write unit tests for `utils.py` channel and node list processing 6f092e5
- [x] Task: Write unit tests for `utils.py` formatting and helper functions 9fa3f3c
- [x] Task: Conductor - User Manual Verification 'Phase 3: Unit Tests for utils.py' (Protocol in workflow.md)

## Phase 4: Unit Tests for config_io.py [checkpoint: c1178ea]
- [x] Task: Write unit tests for `config_io.py` YAML export logic 4501978
- [x] Task: Write unit tests for `config_io.py` YAML import logic 4501978
- [x] Task: Conductor - User Manual Verification 'Phase 4: Unit Tests for config_io.py' (Protocol in workflow.md)
