# Specification: Establishment of Test Suite and Core Utility Coverage

## Goal
Establish a robust testing foundation for the Meshtastic Contact project. This includes setting up `pytest` configuration, coverage reporting, and implementing unit tests for the most critical utility modules: `db_handler.py`, `utils.py`, and `config_io.py`.

## Scope
- Configure `pytest` and `pytest-cov` for the project.
- Create a `tests/unit/` directory structure.
- Implement unit tests for `contact/contact/utilities/db_handler.py` (database initialization, message saving, node info updates).
- Implement unit tests for `contact/contact/utilities/utils.py` (channel parsing, node list generation, formatting helpers).
- Implement unit tests for `contact/contact/utilities/config_io.py` (YAML export/import logic).
- Mock `meshtastic` library dependencies where necessary to allow tests to run without hardware.

## Acceptance Criteria
- `pytest` runs and discovers tests in `tests/unit/`.
- `pytest-cov` generates a coverage report.
- `db_handler.py` has >80% code coverage.
- `utils.py` has >80% code coverage.
- `config_io.py` has >80% code coverage.
- All tests pass in a clean environment.
