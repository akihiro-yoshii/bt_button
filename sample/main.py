import argparse
import logging
import time

import bt_button

loglevels = [logging.CRITICAL, logging.ERROR, logging.WARNING,
             logging.INFO, logging.DEBUG]

MAC_AB = "00:00:00:00:00:00"
MAC_BS = "00:00:00:00:00:00"
MAC_PA = "00:00:00:00:00:00"


def parse_args():
    parser = argparse.ArgumentParser()

    args = [
        {"description": "--loglevel",
         "type": int,
         "default": 2,
         "help": "0:critical, 1:error, 2:warning, 3:info, 4:debug"},
    ]

    for c in args:
        desc = c.pop("description")
        parser.add_argument(desc, **c)

    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=loglevels[args.loglevel])

    ab_shutter = bt_button.AbShutter(MAC_AB)
    ab_shutter.attach_button_event_listener(
        bt_button.AbShutterButton.LARGE,
        bt_button.AbShutterButtonEvent.PUSHED, pushed)
    ab_shutter.attach_button_event_listener(
        bt_button.AbShutterButton.LARGE,
        bt_button.AbShutterButtonEvent.KEEP, keep)
    ab_shutter.attach_button_event_listener(
        bt_button.AbShutterButton.LARGE,
        bt_button.AbShutterButtonEvent.RELEASED, released)

    bt_selfie = bt_button.BTselfie(MAC_BS)
    bt_selfie.attach_button_event_listener(
        bt_button.BtSelfieButton.CENTER,
        bt_button.BtSelfieButtonEvent.RELEASED, released)

    smart_palette = bt_button.SmartPalette(MAC_PA)
    smart_palette.attach_pushed_listener(
        bt_button.SmartPaletteButton.RED, pushed)

    while True:
        logging.debug("search ab_shutter")
        if not ab_shutter.is_monitoring():
            try:
                ab_shutter.start_monitor()
            except bt_button.error.DeviceNotFoundError as e:
                logging.debug(e)

        if not bt_selfie.is_monitoring():
            try:
                bt_selfie.start_monitor()
            except bt_button.error.DeviceNotFoundError as e:
                logging.debug(e)

        if not smart_palette.is_connected():
            try:
                smart_palette.connect(timeout=1)
            except bt_button.error.DeviceNotFoundError as e:
                logging.debug(e)

        time.sleep(1)


def pushed(event=None):
    print("Pushed!")


def keep(event=None):
    print("Keep!")


def released(event):
    print("Released!")


if __name__ == '__main__':
    main()
