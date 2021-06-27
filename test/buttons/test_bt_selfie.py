import pytest
from bt_button import BTselfie


@pytest.fixture
def bt_selfie(mocker):
    mocker.patch("bt_button.buttons._device_manager.open_device",
                 return_value=1)
    return BTselfie("00:00:00:00:00:00")


def test_attach_clicked_listener_0(mocker, bt_selfie):
    func = mocker.Mock()
    bt_selfie.attach_clicked_listener(func)

    assert bt_selfie.clicked_func == func


def test_attach_clicked_listener_1(mocker, bt_selfie):
    assert bt_selfie.clicked_func is None


def test_detach_clicked_listener_0(mocker, bt_selfie):
    func = mocker.Mock()
    bt_selfie.attach_clicked_listener(func)

    assert bt_selfie.clicked_func == func

    bt_selfie.detach_clicked_listener()

    assert bt_selfie.clicked_func is None
