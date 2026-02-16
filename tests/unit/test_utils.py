from unittest.mock import MagicMock

from contact.utilities.utils import (
    get_channels,
    get_node_list,
    get_node_num,
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
