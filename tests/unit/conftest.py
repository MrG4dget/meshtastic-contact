import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Add the contact directory to sys.path
sys.path.append(str(Path(__file__).resolve().parents[2] / "contact"))


@pytest.fixture
def temp_db(tmp_path):
    db_path = tmp_path / "test_client.db"
    return str(db_path)


@pytest.fixture
def mock_config(monkeypatch, temp_db):
    import contact.contact.ui.default_config as config

    monkeypatch.setattr(config, "db_file_path", temp_db)
    return config


@pytest.fixture
def mock_interface_state(monkeypatch):
    from contact.contact.utilities.singleton import interface_state

    mock_interface = MagicMock()
    mock_interface.nodes = {}
    monkeypatch.setattr(interface_state, "interface", mock_interface)
    monkeypatch.setattr(interface_state, "my_node_num", 12345678)
    return interface_state


@pytest.fixture
def mock_ui_state(monkeypatch):
    from contact.contact.utilities.singleton import ui_state

    monkeypatch.setattr(ui_state, "all_messages", {})
    monkeypatch.setattr(ui_state, "channel_list", [])
    return ui_state
