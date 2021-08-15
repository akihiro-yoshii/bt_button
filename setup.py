from setuptools import setup

setup(
    name="bt_button",
    version="0.3",
    description="Bluetooth Button Wrapper",
    install_requires=[
        "evdev",
        "pygatt",
    ],
    packages=['bt_button'],
)
