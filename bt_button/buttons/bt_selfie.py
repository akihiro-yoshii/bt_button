import logging
import threading

import evdev
from enum import Enum

from ._device_manager import open_device, remove_device


class BtSelfieButtonEvent(Enum):
    CLICKED = 0


class BtSelfieButton(Enum):
    CENTER = 28


class BTselfie:
    """
    Create instance of BTselfie.

    Parameters
    -------
    mac_addr
        BTselfie's MAC Address
    """
    def __init__(self, mac_addr):
        self.mac_addr = mac_addr
        self.device = None

        self.name = "BTselfie E Keyboard"

        self.button_event_funcs = {}
        for button in list(BtSelfieButton):
            self.button_event_funcs[button] = {}

            for event in list(BtSelfieButtonEvent):
                self.button_event_funcs[button][event] = None

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

    def attach_button_event_listener(self, button, event, func):
        """
        Attach function that be called when button clicked.

        Parameters
        ----------
        func : function(e)
            This function will be called with evdev.events.InputEvent
            when button be clicked.
        """
        self.button_event_funcs[button][event] = func

    def detach_button_event_listener(self, button, event):
        """
        Detach function that be called when button clicked.
        """
        self.button_event_funcs[button][event] = None

    def _run(self):
        path = self.device.path
        try:
            for e in self.device.read_loop():
                logging.debug(e)

                if e.type == evdev.events.EV_KEY:
                    self._key_event(e)

        except OSError:
            self._disconnect()

    def _key_event(self, e):
        button = BtSelfieButton(e.code)
        event = BtSelfieButtonEvent(e.value)

        logging.info("{}: clicked.".format(self.name))
        if self.button_event_funcs[button][event] is not None:
            self.button_event_funcs[button][event](e)
