# Technology Stack - Meshtastic Contact

## Core Runtime
- **Python 3.9+**: The primary programming language for the application logic and TUI.

## Key Libraries and Frameworks
- **Meshtastic (Python SDK)**: The core library for interacting with Meshtastic hardware and the mesh network.
- **Curses**: Used for building the keyboard-driven terminal user interface. windows-curses is used for compatibility on Windows systems.
- **PyYAML**: Used for importing and exporting node configurations.

## Data and Configuration
- **SQLite**: Used for persistent storage of message history and node data.
- **INI Files**: Used for local configuration and user-defined settings (colors, icons, app behavior).

## Infrastructure and Tooling
- **Poetry**: Used for dependency management and packaging.
- **Docker**: Provides a containerized environment for consistent deployment across different platforms.
- **Ruff**: Employed for linting and code formatting to maintain code quality.
- **Pytest**: Used as the testing framework.
- **pytest-cov**: Used for generating code coverage reports.
