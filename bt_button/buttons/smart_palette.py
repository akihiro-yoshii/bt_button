import logging
import threading
import sys
import signal
import struct

from bluepy import btle
from enum import IntEnum


class SmartPaletteButton(IntEnum):
    BEIGE = 3
    YELLOW = 4
    ORANGE = 5
    RED = 1
    PINK = 2
    PURPLE = 9
    LIGHT_GREEN = 10
    GREEN = 11
    CYAN = 7
    BLUE = 8
    BROWN = 21
    BLACK = 22
    SMALL = 23
    MIDDLE = 19
    LARGE = 20
    HOME = 27
    SAVE = 28
    SEND = 29
    BIG_BUTTON = 12


class SmartPalette:
    def __init__(self, mac_addr):
        """
        Create instance of SmartPalette.

        Parameters
        -------
        mac_addr
            SmartPalette's MAC Address
        """
        self.mac_addr = mac_addr
        self.device = None

        self.name = "SmartPalette"

        self.pushed_funcs = {}
        for button in list(SmartPaletteButton):
            self.pushed_funcs[button] = None

        signal.signal(signal.SIGINT, self._terminate)
        signal.signal(signal.SIGTERM, self._terminate)

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
        class MyDelegate(btle.DefaultDelegate):
            def __init__(self, func):
                btle.DefaultDelegate.__init__(self)
                self.func = func

            def handleNotification(self, handle, data):
                self.func(data)

        self.device = btle.Peripheral(self.mac_addr, "random")
        logging.info("{}: connected".format(self.name))
        self.device.setDelegate(MyDelegate(self._event))

        self.device.writeCharacteristic(0x000c, b'\x01\x00', True)

        self.break_flag = False

        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def disconnect(self):
        """
        Disconnect to device and stop to listen button event
        """
        if not self.is_connected():
            return

        self.break_flag = True
        self.thread.join()

        self.device.disconnect()
        self.device = None
        logging.info("{}: disconnected".format(self.name))

    def attach_pushed_listener(self, button, func):
        """
        Attach function that be called when button clicked.

        Parameters
        ----------
        button : SmartPaletteButton
            Enum to identify target button.
        func : function()
            This function will be called when button be clicked.
        """
        self.pushed_funcs[button] = func

    def detach_pushed_listener(self, button):
        """
        Detach function that be called when button clicked.
        """
        self.pushed_funcs[button] = None

    def _terminate(self, signum, frame):
        self.disconnect()
        sys.exit(0)

    def _run(self):
        try:
            while True:
                if self.break_flag:
                    break
                self.device.waitForNotifications(0.5)

        except btle.BTLEDisconnectError:
            self.device = None
            logging.info("{}: disconnected".format(self.name))

    def _event(self, data):
        decoded_data = struct.unpack('5sb', data)[0].decode()
        button_number = int(decoded_data.replace("PIN", ""))
        button = SmartPaletteButton(button_number)

        logging.info("{} : pushed.".format(button))
        if self.pushed_funcs[button] is not None:
            self.pushed_funcs[button]()
