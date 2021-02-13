import evdev


class DeviceManager:
    def __init__(self):
        self.connected_paths = []

    def search_device(self, name):
        devs = evdev.util.list_devices()
        for dev_path in devs:
            if dev_path in self.connected_paths:
                continue

            dev = evdev.InputDevice(dev_path)
            if dev.name != name:
                continue

            return dev.path

        return None

    def open_device(self, path):
        device = evdev.InputDevice(path)
        self.connected_paths.append(path)

        return device


_dev_mgr = DeviceManager()
