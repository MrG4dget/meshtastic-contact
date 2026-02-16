# Plan: Establishment of Test Suite and Core Utility Coverage

## Phase 1: Test Infrastructure Setup [checkpoint: 57a0929]
- [x] Task: Configure pytest and coverage in `pyproject.toml` or `pytest.ini` 6896277
- [x] Task: Create initial test directory structure and `conftest.py` with necessary fixtures 6f06d88
- [x] Task: Conductor - User Manual Verification 'Phase 1: Test Infrastructure Setup' (Protocol in workflow.md)

## Phase 2: Unit Tests for db_handler.py
- [x] Task: Write unit tests for `db_handler.py` covering `init_nodedb` and `save_message_to_db` 6165e66
- [ ] Task: Write unit tests for `db_handler.py` covering node info updates and name retrieval
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Unit Tests for db_handler.py' (Protocol in workflow.md)

## Phase 3: Unit Tests for utils.py
- [ ] Task: Write unit tests for `utils.py` channel and node list processing
- [ ] Task: Write unit tests for `utils.py` formatting and helper functions
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Unit Tests for utils.py' (Protocol in workflow.md)

## Phase 4: Unit Tests for config_io.py
- [ ] Task: Write unit tests for `config_io.py` YAML export logic
- [ ] Task: Write unit tests for `config_io.py` YAML import logic
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Unit Tests for config_io.py' (Protocol in workflow.md)
