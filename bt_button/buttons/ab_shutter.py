import logging
from enum import Enum

from ._event_device import EventDevice

log = logging.getLogger(__name__)


class AbShutterButtonEvent(Enum):
    PUSHED = 1
    RELEASED = 0
    KEEP = 2


class AbShutterButton(Enum):
    LARGE = 115
    SMALL = 28


class AbShutter(EventDevice):
    """
    Create instance of AbShutter.

    Parameters
    ----------
    mac_addr
        AbShutter's MAC Address
    """
    def __init__(self, mac_addr):
        super().__init__(mac_addr, "AB Shutter3")

        self.button_event_funcs = {}
        for button in list(AbShutterButton):
            self.button_event_funcs[button] = {}

            for event in list(AbShutterButtonEvent):
                self.button_event_funcs[button][event] = None

        log.info("{}: initialized".format(self.name))

    def attach_button_event_listener(self, button, event, func):
        """
        Attach function that be called when button pushed.

        Parameters
        ----------
        button : AbShutterButton
            Enum to identify target button
        event : AbShutterButtonEvent
            Enum to identify target event
        func : function(e)
            This function will be called with evdev.events.InputEvent
            when target event happened.
        """
        self.button_event_funcs[button][event] = func

    def detach_button_event_listener(self, button, event):
        """
        Detach function that be called when button event happened.

        Parameters
        ----------
        button : AbShutterButton
            Enum to identify target button
        event : AbShutterButtonEvent
            Enum to identify target event
        """
        self.button_event_funcs[button][event] = None

    def _key_event(self, e):
        button = AbShutterButton(e.code)
        event = AbShutterButtonEvent(e.value)

        log.info("[{}] {}: {}".format(self.name, button, event))

        if self.button_event_funcs[button][event] is not None:
            self.button_event_funcs[button][event](e)
