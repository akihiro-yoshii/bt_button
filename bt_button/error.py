class Error(Exception):
    "Base class for exceptions in this module"
    pass


class DeviceNotFoundError(Error):
    def __init__(self, message, device_name):
        self.message = message
        self.device_name = device_name
