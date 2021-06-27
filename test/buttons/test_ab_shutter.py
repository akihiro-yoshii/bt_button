import pytest
from bt_button import AbShutter


@pytest.fixture
def ab_shutter(mocker):
    mocker.patch("bt_button.buttons._device_manager.open_device",
                 return_value=1)
    return AbShutter("00:00:00:00:00:00")


def test_attach_pushed_listener_0(mocker, ab_shutter):
    func = mocker.Mock()
    ab_shutter.attach_pushed_listener(func)

    assert ab_shutter.pushed_func is not None


def test_attach_pushed_listener_1(mocker, ab_shutter):
    assert ab_shutter.pushed_func is None


def test_detach_pushed_listener_0(mocker, ab_shutter):
    func = mocker.Mock()
    ab_shutter.attach_pushed_listener(func)

    assert ab_shutter.pushed_func == func

    ab_shutter.detach_pushed_listener()

    assert ab_shutter.pushed_func is None


def test_attach_released_listener_0(mocker, ab_shutter):
    func = mocker.Mock()
    ab_shutter.attach_released_listener(func)

    assert ab_shutter.released_func is not None


def test_attach_released_listener_1(mocker, ab_shutter):
    assert ab_shutter.released_func is None


def test_detach_released_listener_0(mocker, ab_shutter):
    func = mocker.Mock()
    ab_shutter.attach_released_listener(func)

    assert ab_shutter.released_func == func

    ab_shutter.detach_released_listener()

    assert ab_shutter.released_func is None
