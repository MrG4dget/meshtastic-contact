from dataclasses import dataclass, field
from typing import Any, Union


@dataclass
class MenuState:
    menu_index: list[int] = field(default_factory=list)
    start_index: list[int] = field(default_factory=lambda: [0])
    selected_index: int = 0
    current_menu: Union[dict[str, Any], list[Any], str, int] = field(default_factory=dict)
    menu_path: list[str] = field(default_factory=list)
    show_save_option: bool = False
    need_redraw: bool = False


@dataclass
class ChatUIState:
    display_log: bool = False
    channel_list: list[str] = field(default_factory=list)
    all_messages: dict[str, list[str]] = field(default_factory=dict)
    notifications: list[str] = field(default_factory=list)
    packet_buffer: list[str] = field(default_factory=list)
    node_list: list[str] = field(default_factory=list)
    selected_channel: int = 0
    selected_message: int = 0
    selected_node: int = 0
    current_window: int = 0
    last_sent_time: float = 0.0
    last_traceroute_time: float = 0.0

    selected_index: int = 0
    start_index: list[int] = field(default_factory=lambda: [0, 0, 0])
    show_save_option: bool = False
    menu_path: list[str] = field(default_factory=list)
    single_pane_mode: bool = False


@dataclass
class InterfaceState:
    interface: Any = None
    my_node_num: int = 0


@dataclass
class AppState:
    lock: Any = None
