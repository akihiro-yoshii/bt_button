import pytest
from bt_button.button import AbShutter


@pytest.fixture
def ab_shutter(mocker):
    mocker.patch("bt_button.button.open_device", return_value=1)
    return AbShutter("00:00:00:00:00:00")


def test_attach_pushed_listener_0(mocker, ab_shutter):
    func = mocker.Mock()
    ab_shutter.attach_pushed_listener(func)

    assert ab_shutter.pushed_func is not None


def test_attach_pushed_listener_1(mocker, ab_shutter):
    assert ab_shutter.pushed_func is None
