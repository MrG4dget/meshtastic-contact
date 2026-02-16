import sqlite3
from unittest.mock import patch

from contact.utilities.db_handler import (
    get_name_from_database,
    get_table_name,
    init_nodedb,
    is_chat_archived,
    load_messages_from_db,
    maybe_store_nodeinfo_in_db,
    save_message_to_db,
    update_ack_nak,
    update_node_info_in_db,
)


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


def test_update_node_info_in_db_upsert(mock_config, mock_interface_state, temp_db):
    user_id = 999
    long_name = "Original Name"

    # Initial insert
    update_node_info_in_db(user_id=user_id, long_name=long_name)

    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        table_name = f'"{mock_interface_state.my_node_num}_nodedb"'
        cursor.execute(f"SELECT long_name FROM {table_name} WHERE user_id = ?", (user_id,))
        assert cursor.fetchone()[0] == long_name

    # Update
    new_name = "Updated Name"
    update_node_info_in_db(user_id=user_id, long_name=new_name)

    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT long_name FROM {table_name} WHERE user_id = ?", (user_id,))
        assert cursor.fetchone()[0] == new_name


def test_get_name_from_database(mock_config, mock_interface_state, temp_db):
    user_id = 555
    short_name = "SN555"
    update_node_info_in_db(user_id=user_id, short_name=short_name)

    # Test short name retrieval
    retrieved_short = get_name_from_database(user_id, type="short")
    assert retrieved_short == short_name

    # Test long name retrieval (should return hex since we didn't set long_name and it defaults)
    retrieved_long = get_name_from_database(user_id, type="long")
    assert retrieved_long is not None
    assert retrieved_long.startswith("Meshtastic ")


def test_update_ack_nak(mock_config, mock_interface_state, temp_db):
    channel = "test_ack"
    user_id = str(mock_interface_state.my_node_num)
    message = "Message to ACK"
    timestamp = save_message_to_db(channel, user_id, message)

    update_ack_nak(channel, timestamp, message, "Ack")

    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        table_name = get_table_name(channel)
        cursor.execute(f"SELECT ack_type FROM {table_name} WHERE timestamp = ?", (timestamp,))
        assert cursor.fetchone()[0] == "Ack"


def test_is_chat_archived(mock_config, mock_interface_state, temp_db):
    update_node_info_in_db(user_id=111, chat_archived=1)
    assert is_chat_archived(111) == 1

    update_node_info_in_db(user_id=222, chat_archived=0)
    assert is_chat_archived(222) == 0

    assert is_chat_archived(999) == 0  # Unknown


def test_maybe_store_nodeinfo_in_db(mock_config, mock_interface_state, temp_db):
    packet = {
        "from": 333,
        "decoded": {
            "user": {
                "longName": "Maybe Name",
                "shortName": "MN",
                "hwModel": "TBEAM",
            }
        },
    }
    maybe_store_nodeinfo_in_db(packet)

    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        table_name = f'"{mock_interface_state.my_node_num}_nodedb"'
        cursor.execute(f"SELECT long_name FROM {table_name} WHERE user_id = ?", (333,))
        assert cursor.fetchone()[0] == "Maybe Name"


def test_load_messages_from_db(mock_config, mock_interface_state, mock_ui_state, temp_db):
    from contact.utilities.db_handler import ensure_node_table_exists

    ensure_node_table_exists()
    channel = "chat"
    user_id = "1234"
    message = "Hello from past"
    save_message_to_db(channel, user_id, message)

    load_messages_from_db()

    # channel 'chat' should be in channel_list
    assert "chat" in mock_ui_state.channel_list
    assert "chat" in mock_ui_state.all_messages
    # Message should be in all_messages['chat']
    messages = mock_ui_state.all_messages["chat"]
    expected_min_messages = 2
    assert len(messages) >= expected_min_messages
    assert messages[1][1] == message


def test_db_errors_handling(mock_config, mock_interface_state, temp_db):
    with patch("sqlite3.connect", side_effect=sqlite3.Error("Mocked DB Error")):
        # Should not raise exception
        assert save_message_to_db("ch", "u", "m") is None
        update_ack_nak("ch", 1, "m", "Ack")
        load_messages_from_db()
        update_node_info_in_db(1)
        assert get_name_from_database(1) == "Unknown"
        assert is_chat_archived(1) == "Unknown"


def test_init_nodedb_no_nodes(mock_config, mock_interface_state, temp_db):
    mock_interface_state.interface.nodes = {}
    init_nodedb()
    # Should just return gracefully


def test_update_node_info_in_db_partial_fields(mock_config, mock_interface_state, temp_db):
    user_id = 123
    update_node_info_in_db(user_id=user_id, long_name="Name", is_licensed=1, chat_archived=1)

    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        table_name = f'"{mock_interface_state.my_node_num}_nodedb"'
        cursor.execute(f"SELECT is_licensed, chat_archived FROM {table_name} WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        assert row[0] == "1"
        assert row[1] == 1

    # Update only chat_archived
    update_node_info_in_db(user_id=user_id, chat_archived=0)
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT long_name, is_licensed, chat_archived FROM {table_name} WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        assert row[0] == "Name"
        assert row[1] == "1"
        assert row[2] == 0
