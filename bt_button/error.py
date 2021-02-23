class Error(Exception):
    "Base class for exceptions in this module"
    pass


class DeviceNotFoundError(Error):
    def __init__(self, message, name, mac_addr):
        self.message = message
        self.name = name
        self.mac_addr = mac_addr
