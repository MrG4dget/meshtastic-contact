import sqlite3

from contact.utilities.db_handler import get_table_name, init_nodedb, save_message_to_db


def test_save_message_to_db_creates_table_and_saves(mock_config, mock_interface_state, temp_db):
    channel = "test_channel"
    user_id = "user123"
    message_text = "Hello World"

    timestamp = save_message_to_db(channel, user_id, message_text)

    assert timestamp is not None

    # Verify in DB
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        table_name = get_table_name(channel)
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        assert len(rows) == 1
        assert rows[0][0] == user_id
        assert rows[0][1] == message_text
        assert rows[0][2] == timestamp


def test_init_nodedb_populates_db(mock_config, mock_interface_state, temp_db):
    # Setup mock nodes
    node1 = {
        "num": 1,
        "user": {
            "longName": "Node One",
            "shortName": "N1",
            "hwModel": "TBEAM",
            "isLicensed": False,
            "role": "ROUTER",
            "publicKey": "key1",
        },
    }
    mock_interface_state.interface.nodes = {1: node1}

    init_nodedb()

    # Verify in DB
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        table_name = f'"{mock_interface_state.my_node_num}_nodedb"'
        cursor.execute(f"SELECT * FROM {table_name} WHERE user_id = ?", (1,))
        row = cursor.fetchone()

        assert row is not None
        assert row[1] == "Node One"
        assert row[2] == "N1"
        assert row[3] == "TBEAM"
