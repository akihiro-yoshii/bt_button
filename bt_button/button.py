import logging
import threading
import sys
import signal

import evdev
from bluepy import btle

from ._device_manager import open_device, remove_device


class AbShutter:
    """
    Create instance of AbShutter.

    Parameters
    ----------
    mac_addr
        AbShutter's MAC Address
    """
    def __init__(self, mac_addr):
        self.mac_addr = mac_addr
        self.device = None

        self.name = "AB Shutter3"

        self.pushed_func = None
        self.released_func = None

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

    def attach_pushed_listener(self, func):
        """
        Attach function that be called when button pushed.

        Parameters
        ----------
        func : function(e)
            This function will be called with evdev.events.InputEvent
            when button be clicked.
        """
        self.pushed_func = func

    def detach_pushed_listener(self):
        """
        Detach function that be called when button pushed.
        """
        self.pushed_func = None

    def attach_released_listener(self, func):
        """
        Attach function that be called when button released.

        Parameters
        ----------
        func : function(e)
            This function will be called with evdev.events.InputEvent
            when button be clicked.
        """
        self.released_func = func

    def detach_released_listener(self):
        """
        Detach function that be called when button pushed.
        """
        self.released_func = None

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
        if (e.code, e.value) in [(115, 1), (28, 1)]:
            logging.info("{}: pushed.".format(self.name))
            self.pushed_func(e)
        else:
            pass

        if (e.code, e.value) in [(115, 0), (28, 0)]:
            logging.info("{}: released.".format(self.name))
            self.released_func(e)
        else:
            pass


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
        print(data)
