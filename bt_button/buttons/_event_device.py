import logging
import threading
import evdev

from .. import DeviceNotFoundError


connected_paths = []


def _search_device(name, mac_addr):
    devs = evdev.util.list_devices()
    for dev_path in devs:
        if dev_path in connected_paths:
            continue

        dev = evdev.InputDevice(dev_path)
        if dev.name == name and dev.uniq == mac_addr:
            return dev

    return None


def open_device(name, mac_addr):
    device = _search_device(name, mac_addr.lower())
    if device is None:
        raise DeviceNotFoundError("Device not found:", name, mac_addr)

    connected_paths.append(device.path)

    return device


def remove_device(path):
    connected_paths.remove(path)


class EventDevice:
    def __init__(self, mac_addr, name):
        self.mac_addr = mac_addr
        self.device = None

        self.name = name

    def is_connected(self):
        logging.warning(
            "Please use is_monitoring() instead of is_connected().")
        return self.is_monitoring()

    def is_monitoring(self):
        """
        Returns True if device is connected
        """
        return self.device is not None

    def connect(self):
        logging.warning("Please use start_monitor() instead of connect().")
        self.start_monitor()

    def start_monitor(self):
        self.device = open_device(self.name, self.mac_addr)
        logging.info("{}: connected".format(self.name))

        self.thread = threading.Thread(target=self._run)
        self.thread.setDaemon(True)
        self.thread.start()

    def _finish_monitor(self):
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
            self._finish_monitor()
