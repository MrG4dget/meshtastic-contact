import json
from unittest.mock import MagicMock, mock_open, patch

import yaml

from contact.utilities.config_io import (
    config_export,
    config_import,
    save_config,
    set_pref,
    split_compound_name,
    traverse_config,
)


def test_config_export(mock_interface_state):
    # Setup mocks
    mock_interface = mock_interface_state.interface
    mock_interface.getLongName.return_value = "Long Name"
    mock_interface.getShortName.return_value = "LN"
    mock_interface.localNode.getURL.return_value = "http://test.url"
    mock_interface.getMyNodeInfo.return_value = {"position": {"latitude": 1.23, "longitude": 4.56, "altitude": 789}}

    # Mock localConfig and moduleConfig
    mock_interface.localNode.localConfig = MagicMock()
    mock_interface.localNode.moduleConfig = MagicMock()

    # Mock MessageToDict
    with patch("contact.utilities.config_io.MessageToDict") as mock_m2d:
        mock_m2d.side_effect = [
            {"network": {"wifi_psk": "password"}},  # localConfig
            {"telemetry": {"enabled": True}},  # moduleConfig
        ]

        yaml_out = config_export(mock_interface)

        # Verify output
        header = "# start of Meshtastic configure yaml\n"
        assert yaml_out.startswith(header)
        parsed = yaml.safe_load(yaml_out.replace(header, ""))

        assert parsed["owner"] == "Long Name"
        assert parsed["owner_short"] == "LN"
        assert parsed["channel_url"] == "http://test.url"
        assert parsed["location"]["lat"] == 1.23  # noqa: PLR2004
        assert parsed["location"]["lon"] == 4.56  # noqa: PLR2004
        assert parsed["location"]["alt"] == 789  # noqa: PLR2004
        assert parsed["config"]["network"]["wifi_psk"] == "password"
        assert parsed["module_config"]["telemetry"]["enabled"] is True


def test_config_export_keys_base64(mock_interface_state):
    mock_interface = mock_interface_state.interface
    mock_interface.getLongName.return_value = None
    mock_interface.getShortName.return_value = None
    mock_interface.localNode.getURL.return_value = None
    mock_interface.getMyNodeInfo.return_value = {}

    # Mock localConfig and moduleConfig
    mock_interface.localNode.localConfig = MagicMock()
    mock_interface.localNode.moduleConfig = MagicMock()

    with patch("contact.utilities.config_io.MessageToDict") as mock_m2d:
        # Testing security key base64 prefixing
        mock_m2d.side_effect = [
            {"security": {"privateKey": "priv", "publicKey": "pub", "adminKey": ["key1", "key2"]}},
            {},  # moduleConfig
        ]

        yaml_out = config_export(mock_interface)
        parsed = yaml.safe_load(yaml_out.replace("# start of Meshtastic configure yaml\n", ""))

        sec = parsed["config"]["security"]
        assert sec["privateKey"] == "base64:priv"
        assert sec["publicKey"] == "base64:pub"
        assert sec["adminKey"] == ["base64:key1", "base64:key2"]


def test_config_export_camel_case(mock_interface_state):
    mock_interface = mock_interface_state.interface
    mock_interface.getLongName.return_value = "Long Name"
    mock_interface.getShortName.return_value = "LN"
    mock_interface.localNode.getURL.return_value = "http://test.url"
    mock_interface.getMyNodeInfo.return_value = {}

    # Mock localConfig and moduleConfig
    mock_interface.localNode.localConfig = MagicMock()
    mock_interface.localNode.moduleConfig = MagicMock()

    with patch("contact.utilities.config_io.mt_config") as mock_mt_config:
        mock_mt_config.camel_case = True

        with patch("contact.utilities.config_io.MessageToDict") as mock_m2d:
            mock_m2d.side_effect = [
                {"network": {"wifi_psk": "password"}},  # localConfig
                {"telemetry": {"enabled": True}},  # moduleConfig
            ]

            yaml_out = config_export(mock_interface)
            parsed = yaml.safe_load(yaml_out.replace("# start of Meshtastic configure yaml\n", ""))

            assert parsed["channelUrl"] == "http://test.url"
            assert "channel_url" not in parsed


def test_split_compound_name():
    assert split_compound_name("lora.modem_preset") == ["lora", "modem_preset"]
    assert split_compound_name("wifi_psk") == ["wifi_psk", "wifi_psk"]


def test_config_import(mock_interface_state):
    mock_interface = mock_interface_state.interface
    yaml_content = """
owner: New Name
ownerShort: NN
channelUrl: http://new.url
location:
  lat: 10.0
  lon: 20.0
  alt: 30
config:
  network:
    wifi_psk: new_password
module_config:
  telemetry:
    enabled: true
"""

    m_open = mock_open(read_data=yaml_content)
    with patch("builtins.open", m_open):
        with patch("contact.utilities.config_io.traverse_config") as mock_traverse:
            config_import(mock_interface, "dummy.yaml")

            # Verify interface calls
            mock_node = mock_interface.getNode.return_value
            mock_node.setOwner.assert_any_call("New Name")
            mock_node.setOwner.assert_any_call(long_name=None, short_name="NN")
            mock_node.setURL.assert_called_with("http://new.url")
            mock_interface.localNode.setFixedPosition.assert_called_with(10.0, 20.0, 30)

            # Verify section processing
            mock_traverse.assert_called()
            mock_node.writeConfig.assert_called()


def test_traverse_config():
    local_config = MagicMock()
    config_data = {
        "wifi": {
            "enabled": True,
        },
        "modem_preset": "LONG_FAST",
    }

    with patch("contact.utilities.config_io.set_pref") as mock_set_pref:
        traverse_config("lora", config_data, local_config)
        mock_set_pref.assert_any_call(local_config, "lora.wifi.enabled", True)
        mock_set_pref.assert_any_call(local_config, "lora.modem_preset", "LONG_FAST")


def test_set_pref_simple():
    mock_config = MagicMock()
    mock_field = MagicMock()
    mock_field.message_type = None
    mock_field.enum_type = None
    mock_field.label = 1  # Not repeated
    mock_field.name = "hop_limit"

    mock_config.DESCRIPTOR.fields_by_name = {"hop_limit": mock_field}

    with patch("contact.utilities.config_io.fromStr", side_effect=lambda x: x):
        set_pref(mock_config, "hop_limit", 3)
        assert mock_config.hop_limit == 3  # noqa: PLR2004


def test_set_pref_nested():
    mock_config = MagicMock()
    mock_network_field = MagicMock()
    mock_network_msg = MagicMock()
    mock_network_field.message_type = mock_network_msg
    mock_network_field.name = "network"

    mock_psk_field = MagicMock()
    mock_psk_field.message_type = None
    mock_psk_field.enum_type = None
    mock_psk_field.label = 1
    mock_psk_field.name = "wifi_psk"

    mock_network_msg.fields_by_name = {"wifi_psk": mock_psk_field}
    mock_config.DESCRIPTOR.fields_by_name = {"network": mock_network_field}

    mock_network_values = MagicMock()
    mock_config.network = mock_network_values

    with patch("contact.utilities.config_io.fromStr", side_effect=lambda x: x):
        set_pref(mock_config, "network.wifi_psk", "password123")
        assert mock_network_values.wifi_psk == "password123"


def test_set_pref_deep_nested():
    mock_config = MagicMock()
    # config -> a -> b -> field
    mock_a_field = MagicMock()
    mock_a_msg = MagicMock()
    mock_a_field.message_type = mock_a_msg
    mock_a_field.name = "a"

    mock_b_field = MagicMock()
    mock_b_msg = MagicMock()
    mock_b_field.message_type = mock_b_msg
    mock_b_field.name = "b"

    mock_leaf_field = MagicMock()
    mock_leaf_field.message_type = None
    mock_leaf_field.enum_type = None
    mock_leaf_field.label = 1
    mock_leaf_field.name = "leaf"

    mock_config.DESCRIPTOR.fields_by_name = {"a": mock_a_field}
    mock_a_msg.fields_by_name = {"b": mock_b_field}
    mock_b_msg.fields_by_name = {"leaf": mock_leaf_field}

    mock_a_values = MagicMock()
    mock_b_values = MagicMock()
    mock_config.a = mock_a_values
    mock_a_values.b = mock_b_values

    with patch("contact.utilities.config_io.fromStr", side_effect=lambda x: x):
        set_pref(mock_config, "a.b.leaf", "value")
        assert mock_b_values.leaf == "value"


def test_set_pref_enum():
    mock_config = MagicMock()
    mock_field = MagicMock()
    mock_field.message_type = None
    mock_enum = MagicMock()
    mock_field.enum_type = mock_enum
    mock_field.label = 1
    mock_field.name = "modem_preset"

    mock_val = MagicMock()
    mock_val.number = 4
    mock_enum.values_by_name.get.return_value = mock_val
    mock_config.DESCRIPTOR.fields_by_name = {"modem_preset": mock_field}

    with patch("contact.utilities.config_io.fromStr", side_effect=lambda x: x):
        set_pref(mock_config, "modem_preset", "LONG_FAST")
        assert mock_config.modem_preset == 4  # noqa: PLR2004


def test_set_pref_enum_invalid():
    mock_config = MagicMock()
    mock_field = MagicMock()
    mock_field.message_type = None
    mock_enum = MagicMock()
    mock_field.enum_type = mock_enum
    mock_field.label = 1
    mock_field.name = "modem_preset"

    mock_enum.values_by_name.get.return_value = None
    mock_enum.values = [MagicMock()]
    mock_enum.values[0].name = "VAL1"
    mock_config.DESCRIPTOR.fields_by_name = {"modem_preset": mock_field}

    with patch("contact.utilities.config_io.fromStr", side_effect=lambda x: x):
        # Should log warning and return False
        assert set_pref(mock_config, "modem_preset", "INVALID") is False


def test_set_pref_repeated_clear():
    mock_config = MagicMock()
    mock_sec_field = MagicMock()
    mock_sec_msg = MagicMock()
    mock_sec_field.message_type = mock_sec_msg
    mock_sec_field.name = "security"

    mock_key_field = MagicMock()
    mock_key_field.message_type = None
    mock_key_field.enum_type = None
    mock_key_field.label = 3  # LABEL_REPEATED
    mock_key_field.LABEL_REPEATED = 3
    mock_key_field.name = "admin_key"

    mock_sec_msg.fields_by_name = {"admin_key": mock_key_field}
    mock_config.DESCRIPTOR.fields_by_name = {"security": mock_sec_field}

    mock_sec_values = MagicMock()
    mock_config.security = mock_sec_values
    mock_sec_values.admin_key = ["old"]

    with patch("contact.utilities.config_io.fromStr", side_effect=lambda x: x):
        # val == 0 should clear
        set_pref(mock_config, "security.admin_key", 0)
        assert len(mock_sec_values.admin_key) == 0


def test_set_pref_repeated_add():
    mock_config = MagicMock()
    mock_sec_field = MagicMock()
    mock_sec_msg = MagicMock()
    mock_sec_field.message_type = mock_sec_msg
    mock_sec_field.name = "security"

    mock_key_field = MagicMock()
    mock_key_field.message_type = None
    mock_key_field.enum_type = None
    mock_key_field.label = 3  # LABEL_REPEATED
    mock_key_field.LABEL_REPEATED = 3
    mock_key_field.name = "admin_key"

    mock_sec_msg.fields_by_name = {"admin_key": mock_key_field}
    mock_config.DESCRIPTOR.fields_by_name = {"security": mock_sec_field}

    mock_sec_values = MagicMock()
    mock_config.security = mock_sec_values
    mock_sec_values.admin_key = ["old"]

    with patch("contact.utilities.config_io.fromStr", side_effect=lambda x: x):
        set_pref(mock_config, "security.admin_key", "new")
        assert "new" in mock_sec_values.admin_key


def test_set_pref_repeated_list():
    mock_config = MagicMock()
    mock_sec_field = MagicMock()
    mock_sec_msg = MagicMock()
    mock_sec_field.message_type = mock_sec_msg
    mock_sec_field.name = "security"

    mock_key_field = MagicMock()
    mock_key_field.message_type = None
    mock_key_field.enum_type = None
    mock_key_field.label = 3  # LABEL_REPEATED
    mock_key_field.LABEL_REPEATED = 3
    mock_key_field.name = "admin_key"

    mock_sec_msg.fields_by_name = {"admin_key": mock_key_field}
    mock_config.DESCRIPTOR.fields_by_name = {"security": mock_sec_field}

    mock_sec_values = MagicMock()
    mock_config.security = mock_sec_values
    mock_sec_values.admin_key = ["old"]

    with patch("contact.utilities.config_io.fromStr", side_effect=lambda x: x):
        set_pref(mock_config, "security.admin_key", ["key1", "key2"])
        assert mock_sec_values.admin_key == ["key1", "key2"]


def test_set_pref_type_error():
    mock_config = MagicMock()
    mock_field = MagicMock()
    mock_field.message_type = None
    mock_field.label = 1
    mock_field.name = "hop_limit"
    mock_config.DESCRIPTOR.fields_by_name = {"hop_limit": mock_field}

    with patch("contact.utilities.config_io.fromStr", side_effect=lambda x: x):
        with patch("contact.utilities.config_io.setattr", side_effect=[TypeError, None]):
            set_pref(mock_config, "hop_limit", 3)  # noqa: PLR2004
            # Should have tried setting it as string in second call


def test_save_config(mock_interface_state):
    mock_interface = mock_interface_state.interface
    config_data = {
        "owner": "New Name",
        "ownerShort": "NN",
        "channel_url": "http://new.url",
        "config": {"network": {"wifi_psk": "new_password"}},
        "module_config": {"telemetry": {"enabled": True}},
    }

    m_open = mock_open(read_data=json.dumps(config_data))
    with patch("builtins.open", m_open):
        with patch("contact.utilities.config_io.traverse_config") as mock_traverse:
            save_config(mock_interface)

            mock_node = mock_interface.getNode.return_value
            mock_node.setOwner.assert_any_call(long_name="New Name")
            mock_node.setOwner.assert_any_call(long_name=None, short_name="NN")

            mock_traverse.assert_called()


def test_set_pref_wifi_psk_short():
    mock_config = MagicMock()
    mock_field = MagicMock()
    mock_field.name = "wifi_psk"
    mock_config.DESCRIPTOR.fields_by_name = {"wifi_psk": mock_field}

    # PSK < 8 chars
    assert set_pref(mock_config, "wifi_psk", "short") is False
