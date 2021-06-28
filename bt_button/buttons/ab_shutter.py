import logging
import threading

import evdev
from enum import IntEnum

from ._device_manager import open_device, remove_device


class AbShutterButtonEvent(IntEnum):
    PUSHED = 1
    RELEASED = 0
    KEEP = 2


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
        for button_event in list(AbShutterButtonEvent):
            self.button_event_funcs[button_event] = None

        logging.info("{}: initialized".format(self.name))

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
        logging.info("{}: connected".format(self.name))

        self.thread = threading.Thread(target=self._run)
        self.thread.setDaemon(True)
        self.thread.start()

    def _disconnect(self):
        remove_device(self.device.path)
        self.device = None
        logging.info("{}: disconnected".format(self.name))

    def attach_button_event_listener(self, button_event, func):
        """
        Attach function that be called when button pushed.

        Parameters
        ----------
        button_event : ABShutterButtonEvent
            Enum to identify target event
        func : function(e)
            This function will be called with evdev.events.InputEvent
            when target event happened.
        """
        self.button_event_funcs[button_event] = func

    def detach_button_event_listener(self, button_event):
        """
        Detach function that be called when button event happened.
        """
        self.button_event_funcs[button_event] = None

    def _run(self):
        try:
            for e in self.device.read_loop():
                logging.debug(e)

                if e.type == evdev.events.EV_KEY:
                    self._key_event(e)
        except OSError:
            self._disconnect()

    def _key_event(self, e):
        event = AbShutterButtonEvent(e.value)

        if (e.code, e.value) in [(115, 1), (28, 1)]:
            logging.info("{}: pushed.".format(self.name))

        if (e.code, e.value) in [(115, 0), (28, 0)]:
            logging.info("{}: released.".format(self.name))

        if (e.code, e.value) in [(115, 2), (28, 2)]:
            logging.info("{}: keep.".format(self.name))

        if self.button_event_funcs[event] is not None:
            self.button_event_funcs[event](e)
