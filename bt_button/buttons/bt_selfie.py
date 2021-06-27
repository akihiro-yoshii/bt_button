import logging
import threading

import evdev

from ._device_manager import open_device, remove_device


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

        self.clicked_func = None

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

    def attach_clicked_listener(self, func):
        """
        Attach function that be called when button clicked.

        Parameters
        ----------
        func : function(e)
            This function will be called with evdev.events.InputEvent
            when button be clicked.
        """
        self.clicked_func = func

    def detach_clicked_listener(self):
        """
        Detach function that be called when button clicked.
        """
        self.clicked_func = None

    def _run(self):
        path = self.device.path
        try:
            for e in self.device.read_loop():
                logging.debug(e)

                if e.type == evdev.events.EV_KEY:
                    self._key_event(e)

        except OSError:
            self.device = None
            remove_device(path)
            logging.info("{}: disconnected".format(self.name))

    def _key_event(self, e):
        if (e.code, e.value) == (28, 0):
            logging.info("{}: clicked.".format(self.name))
            self.clicked_func(e)
        else:
            pass
