import datetime
from unittest.mock import MagicMock, patch

from contact.utilities.utils import (
    add_new_message,
    convert_to_camel_case,
    decimal_to_hex,
    get_channels,
    get_node_list,
    get_node_num,
    get_readable_duration,
    get_time_ago,
    get_time_val_units,
    parse_protobuf,
    refresh_node_list,
)


def test_get_channels(mock_interface_state, mock_ui_state):
    # Setup mock local node channels
    mock_node = MagicMock()
    channel0 = MagicMock()
    channel0.role = 1  # PRIMARY
    channel0.settings.name = "Default"

    channel1 = MagicMock()
    channel1.role = 2  # SECONDARY
    channel1.settings.name = "Private"

    mock_node.channels = [channel0, channel1]
    mock_interface_state.interface.getNode.return_value = mock_node

    channels = get_channels()

    assert "Default" in channels
    assert "Private" in channels
    assert "Default" in mock_ui_state.all_messages
    assert "Private" in mock_ui_state.all_messages


def test_get_channels_blank_name(mock_interface_state, mock_ui_state):
    mock_node = MagicMock()
    channel0 = MagicMock()
    channel0.role = 1
    channel0.settings.name = ""  # Blank name

    # Mock modem preset
    mock_node.localConfig.lora.modem_preset = 0  # LONG_FAST

    mock_node.channels = [channel0]
    mock_interface_state.interface.getNode.return_value = mock_node

    mock_ui_state.channel_list = []

    with patch("contact.utilities.utils.config_pb2") as mock_config_pb2:
        mock_val = MagicMock()
        mock_val.name = "LONG_FAST"
        mock_config_pb2._CONFIG_LORACONFIG_MODEMPRESET.values_by_number = {0: mock_val}

        channels = get_channels()
        assert "LongFast" in channels


def test_get_node_list(mock_interface_state):
    my_node = 12345678
    node1_num = 1
    node2_num = 2
    node1 = {"num": node1_num, "lastHeard": 100, "user": {"longName": "Node1"}}
    node2 = {"num": node2_num, "lastHeard": 200, "user": {"longName": "Node2"}}

    mock_interface_state.my_node_num = my_node
    mock_interface_state.interface.nodes = {my_node: {"num": my_node}, node1_num: node1, node2_num: node2}

    node_list = get_node_list()

    # My node should be first
    assert node_list[0] == my_node
    # Others sorted by lastHeard (descending in get_node_list because of -node["lastHeard"])
    # 200 is > 100, so 2 should come before 1
    assert node_list[1] == node2_num
    assert node_list[2] == node1_num


def test_get_node_list_sort_name(mock_interface_state):
    with patch("contact.ui.default_config.node_sort", "name"):
        my_node = 12345678
        node_me = {"num": my_node, "user": {"longName": "Me"}}
        node1 = {"num": 1, "user": {"longName": "Zebra"}}
        node2 = {"num": 2, "user": {"longName": "Apple"}}
        mock_interface_state.my_node_num = my_node
        mock_interface_state.interface.nodes = {my_node: node_me, 1: node1, 2: node2}

        node_list = get_node_list()
        # Me is always first, then Apple (2), then Zebra (1)
        assert node_list == [my_node, 2, 1]


def test_get_node_list_sort_hops(mock_interface_state):
    with patch("contact.ui.default_config.node_sort", "hops"):
        my_node = 12345678
        node1 = {"num": 1, "hopsAway": 2, "user": {"longName": "N1"}}
        node2 = {"num": 2, "hopsAway": 1, "user": {"longName": "N2"}}
        mock_interface_state.my_node_num = my_node
        mock_interface_state.interface.nodes = {my_node: {"num": my_node}, 1: node1, 2: node2}

        node_list = get_node_list()
        assert node_list == [my_node, 2, 1]


def test_get_node_list_empty(mock_interface_state):
    mock_interface_state.interface.nodes = None
    assert get_node_list() == []


def test_refresh_node_list(mock_interface_state, mock_ui_state):
    my_node = 12345678
    mock_interface_state.my_node_num = my_node
    mock_interface_state.interface.nodes = {my_node: {"num": my_node}}
    mock_ui_state.node_list = []

    changed = refresh_node_list()

    assert changed is True
    assert mock_ui_state.node_list == [my_node]

    # Run again, should not change
    changed_again = refresh_node_list()
    assert changed_again is False


def test_get_node_num(mock_interface_state):
    expected_num = 8888
    mock_interface_state.interface.getMyNodeInfo.return_value = {"num": expected_num}
    assert get_node_num() == expected_num


def test_decimal_to_hex():
    assert decimal_to_hex(255) == "!000000ff"
    assert decimal_to_hex(4026531840) == "!f0000000"


def test_convert_to_camel_case():
    assert convert_to_camel_case("very_long_range_slow") == "VeryLongRangeSlow"
    assert convert_to_camel_case("test") == "Test"


def test_get_time_val_units():
    # Test all branches of get_time_val_units
    assert get_time_val_units(datetime.timedelta(days=400)) == (1, "y")
    assert get_time_val_units(datetime.timedelta(days=365)) == (1, "y")
    assert get_time_val_units(datetime.timedelta(days=31)) == (1, "mon")
    assert get_time_val_units(datetime.timedelta(days=30)) == (1, "mon")
    assert get_time_val_units(datetime.timedelta(days=8)) == (1, "w")
    assert get_time_val_units(datetime.timedelta(days=7)) == (1, "w")
    assert get_time_val_units(datetime.timedelta(days=1)) == (1, "d")
    assert get_time_val_units(datetime.timedelta(hours=2)) == (2, "h")
    assert get_time_val_units(datetime.timedelta(minutes=5)) == (5, "min")
    assert get_time_val_units(datetime.timedelta(seconds=10)) == (10, "s")


def test_get_readable_duration():
    assert get_readable_duration(30) == "30 s"
    assert get_readable_duration(120) == "2 min"
    assert get_readable_duration(7200) == "2 h"
    assert get_readable_duration(86400) == "1 d"
    assert get_readable_duration(86400 * 7) == "1 w"
    assert get_readable_duration(86400 * 29) == "4 w"
    assert get_readable_duration(86400 * 30) == "1 mon"
    assert get_readable_duration(86400 * 31) == "1 mon"
    assert get_readable_duration(86400 * 364) == "12 mon"
    assert get_readable_duration(86400 * 365) == "1 y"
    assert get_readable_duration(86400 * 366) == "1 y"


def test_get_time_ago():
    now = datetime.datetime.now()
    ts_now = now.timestamp()
    assert get_time_ago(ts_now) == "now"

    ts_10m_ago = (now - datetime.timedelta(minutes=10)).timestamp()
    assert get_time_ago(ts_10m_ago) == "10 min ago"


def test_add_new_message(mock_ui_state):
    channel_id = "test_ch"
    prefix = ">>"
    message = "Test message"

    fixed_now = datetime.datetime(2026, 2, 16, 14, 5, 0)
    with patch("time.time", return_value=fixed_now.timestamp()):
        add_new_message(channel_id, prefix, message)

        assert channel_id in mock_ui_state.all_messages
        msgs = mock_ui_state.all_messages[channel_id]
        assert len(msgs) == 2  # noqa: PLR2004
        assert msgs[0][0] == "-- 2026-02-16 14:00 --"
        assert msgs[1][1] == message

        # Add another message in the same hour
        with patch("time.time", return_value=fixed_now.timestamp() + 60):
            add_new_message(channel_id, prefix, "Second message")

        assert len(mock_ui_state.all_messages[channel_id]) == 3  # noqa: PLR2004
        # Should not have added a new hour header
        assert mock_ui_state.all_messages[channel_id][2][1] == "Second message"


def test_parse_protobuf_special_apps():
    # Test special app portnums
    assert parse_protobuf({"decoded": {"portnum": "TEXT_MESSAGE_APP", "payload": b""}}) == "✉️"
    assert parse_protobuf({"decoded": {"portnum": "NODEINFO_APP", "payload": b""}}) == "Name identification payload"
    assert parse_protobuf({"decoded": {"portnum": "TRACEROUTE_APP", "payload": b""}}) == "Traceroute payload"


def test_parse_protobuf_invalid_packet():
    # Test overall exception or None
    assert parse_protobuf(None) is None
    assert parse_protobuf({}) is None


def test_parse_protobuf_string_payload():
    packet = {"decoded": {"portnum": "TEXT_MESSAGE_APP", "payload": "Already a string"}}
    assert parse_protobuf(packet) == "Already a string"


def test_parse_protobuf_position():
    mock_pb = MagicMock()
    mock_handler = MagicMock()
    mock_handler.protobufFactory.return_value = mock_pb

    with patch("contact.utilities.utils.protocols") as mock_protocols:
        mock_protocols.get.return_value = mock_handler
        with patch("contact.utilities.utils.portnums_pb2.PortNum.Value", return_value=1):
            with patch("contact.utilities.telemetry_beautifier.get_chunks", return_value="pos_beautified"):
                packet = {"decoded": {"portnum": "POSITION_APP", "payload": b"data"}}
                assert parse_protobuf(packet) == "pos_beautified"


def test_parse_protobuf_fallback():
    mock_pb = MagicMock()
    # Mocking string representation
    mock_pb.__str__.return_value = "proto_string\nwith_newline"
    mock_pb.HasField.return_value = False

    mock_handler = MagicMock()
    mock_handler.protobufFactory.return_value = mock_pb

    with patch("contact.utilities.utils.protocols") as mock_protocols:
        mock_protocols.get.return_value = mock_handler
        with patch("contact.utilities.utils.portnums_pb2.PortNum.Value", return_value=1):
            packet = {"decoded": {"portnum": "ADMIN_APP", "payload": b"data"}}
            # Should replace \n with space and strip
            assert parse_protobuf(packet) == "proto_string with_newline"


def test_get_node_list_sort_default(mock_interface_state):
    with patch("contact.ui.default_config.node_sort", "unknown"):
        my_node = 12345678
        mock_interface_state.my_node_num = my_node
        # Use only one node to avoid dict-to-dict comparison in sorted()
        mock_interface_state.interface.nodes = {my_node: {"num": my_node}}

        node_list = get_node_list()
        assert node_list == [my_node]


def test_add_new_message_no_header(mock_ui_state):
    channel_id = "test_ch"
    # Pre-populate without header
    mock_ui_state.all_messages[channel_id] = [("just a msg", "content")]

    fixed_now = datetime.datetime(2026, 2, 16, 14, 5, 0)
    with patch("time.time", return_value=fixed_now.timestamp()):
        add_new_message(channel_id, ">>", "New message")

    msgs = mock_ui_state.all_messages[channel_id]
    # Should have added a header because none was found
    assert msgs[1][0] == "-- 2026-02-16 14:00 --"


def test_parse_protobuf_decode_error():
    mock_handler = MagicMock()
    mock_pb = mock_handler.protobufFactory.return_value
    from google.protobuf.message import DecodeError

    mock_pb.ParseFromString.side_effect = DecodeError("fail")

    with patch("contact.utilities.utils.protocols") as mock_protocols:
        mock_protocols.get.return_value = mock_handler
        with patch("contact.utilities.utils.portnums_pb2.PortNum.Value", return_value=1):
            packet = {"decoded": {"portnum": "OTHER_APP", "payload": b"data"}}
            # Should return payload on DecodeError
            assert parse_protobuf(packet) == b"data"


def test_parse_protobuf_exception():
    # Trigger the outer exception block
    with patch("contact.utilities.utils.protocols") as mock_protocols:
        mock_protocols.get.side_effect = Exception("critical fail")
        packet = {"decoded": {"portnum": "OTHER_APP", "payload": b"data"}}
        # Should return payload on general exception
        assert parse_protobuf(packet) == b"data"


def test_parse_protobuf_telemetry():
    # Environment metrics
    mock_pb = MagicMock()
    mock_pb.HasField.side_effect = lambda field: field == "environment_metrics"
    mock_pb.environment_metrics = "env_data"

    mock_handler = MagicMock()
    mock_handler.protobufFactory.return_value = mock_pb

    with patch("contact.utilities.utils.protocols") as mock_protocols:
        mock_protocols.get.return_value = mock_handler
        with patch("contact.utilities.utils.portnums_pb2.PortNum.Value", return_value=1):
            with patch("contact.utilities.telemetry_beautifier.get_chunks", return_value="beautified"):
                packet = {"decoded": {"portnum": "TELEMETRY_APP", "payload": b"data"}}
                assert parse_protobuf(packet) == "beautified"

    # Device metrics
    mock_pb.HasField.side_effect = lambda field: field == "device_metrics"
    mock_pb.device_metrics = "dev_data"
    with patch("contact.utilities.utils.protocols") as mock_protocols:
        mock_protocols.get.return_value = mock_handler
        with patch("contact.utilities.utils.portnums_pb2.PortNum.Value", return_value=1):
            with patch("contact.utilities.telemetry_beautifier.get_chunks", return_value="beautified_dev"):
                packet = {"decoded": {"portnum": "TELEMETRY_APP", "payload": b"data"}}
                assert parse_protobuf(packet) == "beautified_dev"
