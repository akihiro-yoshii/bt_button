import evdev
from .. import DeviceNotFoundError


class __EventDeviceManager:
    def __init__(self):
        self.connected_paths = []

    def _search_device(self, name, mac_addr):
        devs = evdev.util.list_devices()
        for dev_path in devs:
            if dev_path in self.connected_paths:
                continue

            dev = evdev.InputDevice(dev_path)
            if dev.name == name and dev.uniq == mac_addr:
                return dev

        return None

    def open_device(self, name, mac_addr):
        device = self._search_device(name, mac_addr.lower())
        if device is None:
            raise DeviceNotFoundError("Device not found:", name, mac_addr)

        self.connected_paths.append(device.path)

        return device

    def remove_device(self, path):
        self.connected_paths.remove(path)

    def reset(self):
        self.connected_paths.clear()


EventDeviceManager = __EventDeviceManager()
