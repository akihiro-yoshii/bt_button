import evdev
from .error import DeviceNotFoundError


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
