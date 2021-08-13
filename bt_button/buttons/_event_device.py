import logging
import threading

import evdev
from ._device_manager import open_device, remove_device


class EventDevice:
    def __init__(self, mac_addr, name):
        self.mac_addr = mac_addr
        self.device = None

        self.name = name

    def is_connected(self):
        """
        Returns True if device is connected
        """
        return self.device is not None

    def connect(self):
        self.device = open_device(self.name, self.mac_addr)
        logging.info("{}: connected".format(self.name))

        self.thread = threading.Thread(target=self._run)
        self.thread.setDaemon(True)
        self.thread.start()

    def _disconnect(self):
        remove_device(self.device.path)
        self.device = None
        logging.info("{}: disconnected".format(self.name))

    def _run(self):
        try:
            for e in self.device.read_loop():
                logging.debug(e)

                if e.type == evdev.events.EV_KEY:
                    self._key_event(e)

        except OSError:
            self._disconnect()
