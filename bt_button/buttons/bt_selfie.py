import logging
from enum import Enum

from ._event_device import EventDevice


class BtSelfieButtonEvent(Enum):
    PUSHED = 1
    RELEASED = 0


class BtSelfieButton(Enum):
    CENTER = 28


class BTselfie(EventDevice):
    """
    Create instance of BTselfie.

    Parameters
    -------
    mac_addr
        BTselfie's MAC Address
    """
    def __init__(self, mac_addr):
        super().__init__(mac_addr, "BTselfie E Keyboard")

        self.button_event_funcs = {}
        for button in list(BtSelfieButton):
            self.button_event_funcs[button] = {}

            for event in list(BtSelfieButtonEvent):
                self.button_event_funcs[button][event] = None

        logging.info("{}: initialized".format(self.name))

    def attach_button_event_listener(self, button, event, func):
        """
        Attach function that be called when button clicked.

        Parameters
        ----------
        func : function(e)
            This function will be called with evdev.events.InputEvent
            when button be clicked.
        """
        self.button_event_funcs[button][event] = func

    def detach_button_event_listener(self, button, event):
        """
        Detach function that be called when button clicked.
        """
        self.button_event_funcs[button][event] = None

    def _key_event(self, e):
        button = BtSelfieButton(e.code)
        event = BtSelfieButtonEvent(e.value)

        logging.info("{}: clicked.".format(self.name))
        if self.button_event_funcs[button][event] is not None:
            self.button_event_funcs[button][event](e)
