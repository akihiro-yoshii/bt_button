import logging
import threading
import sys
import signal

import evdev
from bluepy import btle

from ._device_manager import open_device, remove_device


class AbShutter:
    def __init__(self, mac_addr):
        """
        Create instance of AbShutter.

        Parameters
        ----------
        mac_addr
            AbShutter's MAC Address
        """
        self.mac_addr = mac_addr
        self.device = None

        self.name = "AB Shutter3"

        self.pushed_funcs = []
        self.released_funcs = []

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

    def _run(self):
        path = self.device.path
        try:
            for e in self.device.read_loop():
                logging.debug(e)

                if e.type == evdev.events.EV_KEY:
                    self._key_event(e)
        except OSError as e:
            self.device = None
            remove_device(path)
            logging.info("{}: disconnected".format(self.name))

    def _key_event(self, e):
        if (e.code, e.value) in [(115, 1), (28, 1)]:
            logging.info("{}: pushed.".format(self.name))
            for f in self.pushed_funcs:
                f(e)
        else:
            pass

        if (e.code, e.value) in [(115, 0), (28, 0)]:
            logging.info("{}: released.".format(self.name))
            for f in self.released_funcs:
                f(e)
        else:
            pass

    def add_pushed_listener(self, func):
        self.pushed_funcs.append(func)

    def add_released_listener(self, func):
        self.released_funcs.append(func)


class BTselfie:
    def __init__(self, mac_addr):
        """
        Create instance of BTselfie.

        Parameters
        -------
        mac_addr
            BTselfie's MAC Address
        """
        self.mac_addr = mac_addr
        self.device = None

        self.name = "BTselfie E Keyboard"

        self.clicked_funcs = []

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

    def _run(self):
        path = self.device.path
        try:
            for e in self.device.read_loop():
                logging.debug(e)

                if e.type == evdev.events.EV_KEY:
                    self._key_event(e)

        except OSError as e:
            self.device = None
            remove_device(path)
            logging.info("{}: disconnected".format(self.name))

    def _key_event(self, e):
        if (e.code, e.value) == (28, 0):
            logging.info("{}: clicked.".format(self.name))
            for f in self.clicked_funcs:
                f(e)
        else:
            pass

    def add_clicked_listener(self, func):
        """
        Register function that be called when button clicked.

        Parameters
        ----------
        func : function(e)
            This function will be called with evdev.events.InputEvent
            when button be clicked.

        Returns
        -------
        None
        """
        self.clicked_funcs.append(func)


class SmartPalette:
    def __init__(self, mac_addr):
        """
        Create instance of BTselfie.

        Parameters
        -------
        mac_addr
            BTselfie's MAC Address
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

        except btle.BTLEDisconnectError as e:
            self.device = None
            logging.info("{}: disconnected".format(self.name))

    def _event(self, data):
        print(data)
