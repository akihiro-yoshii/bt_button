import logging

import threading
import evdev

from ._device_manager import open_device


class AbShutter:
    def __init__(self, mac_addr):
        self.mac_addr = mac_addr
        self.device = None

        self.name = "AB Shutter3"

        self.pushed_funcs = []
        self.released_funcs = []

        logging.info("{}: initialized".format(self.name))

    def is_connected(self):
        return self.device is not None

    def connect(self):
        self.device = open_device(self.name, self.mac_addr)
        logging.info("{}: connected".format(self.name))

        self.thread = threading.Thread(target=self._run)
        self.thread.setDaemon(True)
        self.thread.start()

    def _run(self):
        for e in self.device.read_loop():
            logging.debug(e)

            if e.type == evdev.events.EV_KEY:
                self._key_event(e)

    def _key_event(self, e):
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


class BTselfie:
    def __init__(self, mac_addr):
        """
        Create instance of BTselfie.

        Parameters
        -------
        mac_addr
            BTselfie's MAC Address
        """
        self.mac_addr = mac_addr
        self.device = None

        self.name = "BTselfie E"

        self.clicked_funcs = []

        logging.info("{}: initialized".format(self.name))

    def is_connected(self):
        return self.device is not None

    def connect(self):
        self.device = open_device(self.name, self.mac_addr)
        logging.info("{}: connected".format(self.name))

        self.thread = threading.Thread(target=self._run)
        self.thread.setDaemon(True)
        self.thread.start()

    def _run(self):
        for e in self.device.read_loop():
            logging.debug(e)

            if e.type == evdev.events.EV_KEY:
                self._key_event(e)

    def _key_event(self, e):
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
