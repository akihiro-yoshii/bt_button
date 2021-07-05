import logging
import threading

import evdev
from enum import Enum

from ._device_manager import open_device, remove_device

log = logging.getLogger(__name__)


class AbShutterButtonEvent(Enum):
    PUSHED = 1
    RELEASED = 0
    KEEP = 2


class AbShutterButton(Enum):
    LARGE = 115
    SMALL = 28


class AbShutter:
    """
    Create instance of AbShutter.

    Parameters
    ----------
    mac_addr
        AbShutter's MAC Address
    """
    def __init__(self, mac_addr):
        self.mac_addr = mac_addr
        self.device = None

        self.name = "AB Shutter3"

        self.button_event_funcs = {}
        for button in list(AbShutterButton):
            self.button_event_funcs[button] = {}

            for event in list(AbShutterButtonEvent):
                self.button_event_funcs[button][event] = None

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
        self.device = open_device(self.name, self.mac_addr)
        log.info("{}: connected".format(self.name))

        self.thread = threading.Thread(target=self._run)
        self.thread.setDaemon(True)
        self.thread.start()

    def _disconnect(self):
        remove_device(self.device.path)
        self.device = None
        log.info("{}: disconnected".format(self.name))

    def attach_button_event_listener(self, button, event, func):
        """
        Attach function that be called when button pushed.

        Parameters
        ----------
        button : AbShutterButton
            Enum to identify target button
        event : AbShutterButtonEvent
            Enum to identify target event
        func : function(e)
            This function will be called with evdev.events.InputEvent
            when target event happened.
        """
        self.button_event_funcs[button][event] = func

    def detach_button_event_listener(self, button, event):
        """
        Detach function that be called when button event happened.
        """
        self.button_event_funcs[button][event] = None

    def _run(self):
        try:
            for e in self.device.read_loop():
                log.debug(e)

                if e.type == evdev.events.EV_KEY:
                    self._key_event(e)
        except OSError:
            self._disconnect()

    def _key_event(self, e):
        button = AbShutterButton(e.code)
        event = AbShutterButtonEvent(e.value)

        log.info("[{}] {}: {}".format(self.name, button, event))

        if self.button_event_funcs[button][event] is not None:
            self.button_event_funcs[button][event](e)
