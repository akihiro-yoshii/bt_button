import logging

import threading
import evdev

from .error import DeviceNotFoundError
from ._device_manager import _dev_mgr


def open_device(device_name):
    path = _dev_mgr.search_device(device_name)
    if path is None:
        raise DeviceNotFoundError("Device not found:", device_name)

    return _dev_mgr.open_device(path)


class AbShutter(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)

        self.device = open_device("AB Shutter3")
        self.name = "[AB Shutter]"

        self.pushed_funcs = []
        self.released_funcs = []

        logging.info("{}: initialized".format(self.name))

    def run(self):
        for event in self.device.read_loop():
            self.event(event)

    def event(self, e):
        logging.debug(e)

        if e.type == evdev.events.EV_KEY:
            self.key_event(e)

    def key_event(self, e):
        if (e.code, e.value) in [(115, 1), (28, 1)]:
            logging.info("{}: pushed.".format(self.name))
            for f in self.pushed_funcs:
                f(e)
        else:
            pass

        if (e.code, e.value) in [(115, 0), (28, 0)]:
            logging.info("{}: released.".format(self.name))
            for f in self.released_funcs:
                f(e)
        else:
            pass

    def add_pushed_listener(self, func):
        self.pushed_funcs.append(func)

    def add_released_listener(self, func):
        self.released_funcs.append(func)


class BTselfie(threading.Thread):
    def __init__(self):
        """
        Create instance of BTselfie and connect to the button.

        Raises
        -------
        bt_button.DeviceNotFoundError
            Raises DeviceNotFoundError if the button is not found.
        """
        super().__init__(daemon=True)

        self.device = open_device("BTselfie E")
        self.name = "[BT selfie ]"

        self.clicked_funcs = []

        logging.info("{}: initialized".format(self.name))

    def run(self):
        for event in self.device.read_loop():
            self.event(event)

    def event(self, e):
        logging.debug(e)

        if e.type == evdev.events.EV_KEY:
            self.key_event(e)

    def key_event(self, e):
        if (e.code, e.value) == (115, 0):
            logging.info("{}: clicked.".format(self.name))
            for f in self.clicked_funcs:
                f(e)
        else:
            pass

    def add_clicked_listener(self, func):
        """
        Register function that be called when button clicked.

        Parameters
        ----------
        func : function(e)
            This function will be called with evdev.events.InputEvent
            when button be clicked.

        Returns
        -------
        None
        """
        self.clicked_funcs.append(func)
