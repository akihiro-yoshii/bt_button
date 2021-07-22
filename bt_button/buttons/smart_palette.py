import logging
import struct

import pygatt
from enum import Enum

from .. import DeviceNotFoundError

log = logging.getLogger(__name__)


class SmartPaletteButton(Enum):
    BEIGE = 3
    YELLOW = 4
    ORANGE = 5
    RED = 1
    PINK = 2
    PURPLE = 9
    LIGHT_GREEN = 10
    GREEN = 11
    CYAN = 7
    BLUE = 8
    BROWN = 21
    BLACK = 22
    SMALL = 23
    MIDDLE = 19
    LARGE = 20
    HOME = 27
    SAVE = 28
    SEND = 29
    BIG_BUTTON = 12


def _data_to_button(data):
    decoded_data = struct.unpack('5sb', data)[0].decode()
    button_number = int(decoded_data.replace("PIN", ""))
    return SmartPaletteButton(button_number)


def _button_to_data(button):
    data_str = "PIN{:02}".format(button.value)
    return struct.pack("5s", data_str.encode('utf-8')) + b'\x00'


class SmartPalette:
    def __init__(self, mac_addr):
        """
        Create instance of SmartPalette.

        Parameters
        -------
        mac_addr
            SmartPalette's MAC Address
        """
        self.mac_addr = mac_addr
        self.device = None

        self.name = "SmartPalette"

        self.pushed_funcs = {}
        for button in list(SmartPaletteButton):
            self.pushed_funcs[button] = None

        self.adapter = pygatt.GATTToolBackend()

        self.adapter.start()

        log.info("{}: initialized".format(self.name))

    def is_connected(self):
        """
        Returns True if device is connected
        """
        return self.device is not None

    def connect(self):
        """
        Connect to device and start to listen button event
        """
        try:
            self.device = self.adapter.connect(
                self.mac_addr,
                address_type=pygatt.BLEAddressType.random,
            )
        except pygatt.exceptions.NotConnectedError:
            raise DeviceNotFoundError(
                "Device not found:", self.name, self.mac_addr)

        log.info("{}: connected".format(self.name))

        # self.device.char_write_handle(12, bytearray([0x01, 0x00]))
        self.device.subscribe("6e400003-b5a3-f393-e0a9-e50e24dcca9e",
                              callback=self._event)

    def disconnect(self):
        """
        Disconnect to device and stop to listen button event
        """
        if not self.is_connected():
            return

        self.device.disconnect()
        self.device = None
        self.adapter.stop()
        log.info("{}: disconnected".format(self.name))

    def attach_pushed_listener(self, button, func):
        """
        Attach function that be called when button clicked.

        Parameters
        ----------
        button : SmartPaletteButton
            Enum to identify target button.
        func : function()
            This function will be called when button be clicked.
        """
        self.pushed_funcs[button] = func

    def detach_pushed_listener(self, button):
        """
        Detach function that be called when button clicked.
        """
        self.pushed_funcs[button] = None

    def _event(self, _, data):
        button = _data_to_button(data)

        log.info("{} : pushed.".format(button))
        if self.pushed_funcs[button] is not None:
            self.pushed_funcs[button]()
