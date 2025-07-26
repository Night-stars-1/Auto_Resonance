# nemu.pyi
from typing import Union
from ctypes import (
    CDLL,
    Array,
    c_int,
    c_ubyte,
    _Pointer
)

def init(path: str) -> "NemuDLL": ...

class NemuDLL(CDLL):
    # Connection management
    def nemu_connect(self, path: str, index: int) -> int: ...
    def nemu_disconnect(self, handle: int) -> None: ...
    
    # Display management
    def nemu_get_display_id(self, handle: int, pkg: bytes, appIndex: int) -> int: ...
    def nemu_capture_display(
        self,
        handle: int,
        displayid: int,
        buffer_size: int,
        width: _Pointer[c_int],
        height: _Pointer[c_int],
        pixels: Union[_Pointer[c_ubyte], _Pointer[Array[c_ubyte]]]
    ) -> int: ...
    
    # Input methods
    def nemu_input_text(self, handle: int, size: int, buf: str) -> int: ...
    
    # Touch events
    def nemu_input_event_touch_down(self, handle: int, displayid: int, x_point: int, y_point: int) -> int: ...
    def nemu_input_event_touch_up(self, handle: int, displayid: int) -> int: ...
    
    # Finger events (multi-touch)
    def nemu_input_event_finger_touch_down(
        self,
        handle: int,
        displayid: int,
        finger_id: int,
        x_point: int,
        y_point: int
    ) -> int: ...
    def nemu_input_event_finger_touch_up(self, handle: int, displayid: int, slot_id: int) -> int: ...
    
    # Keyboard events
    def nemu_input_event_key_down(self, handle: int, displayid: int, key_code: int) -> int: ...
    def nemu_input_event_key_up(self, handle: int, displayid: int, key_code: int) -> int: ...
