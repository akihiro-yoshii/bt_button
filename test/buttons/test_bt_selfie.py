import pytest
from bt_button import BTselfie, DeviceNotFoundError
# from bt_button.buttons._device_manager import open_device


@pytest.fixture
def bt_selfie(mocker):
    return BTselfie("00:00:00:00:00:00")


def test_is_connected_0(mocker, bt_selfie):
    bt_selfie.device = mocker.Mock()
    assert bt_selfie.is_connected()


def test_is_connected_1(mocker, bt_selfie):
    assert not bt_selfie.is_connected()


def test_connect_0(mocker, bt_selfie):
    open_device_mock = mocker.patch(
        "bt_button.buttons.bt_selfie.open_device")

    bt_selfie.connect()

    open_device_mock.assert_called_once()


def test_connect_1(mocker, bt_selfie):
    open_device_mock = mocker.patch(
        "bt_button.buttons.bt_selfie.open_device")
    open_device_mock.side_effect = DeviceNotFoundError(
        "hoge", bt_selfie.name, bt_selfie.mac_addr)

    with pytest.raises(DeviceNotFoundError):
        bt_selfie.connect()

    open_device_mock.assert_called_once()


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


def test_key_event_call_target_func(mocker, bt_selfie):
    target_func = mocker.Mock()
    bt_selfie.attach_clicked_listener(target_func)

    bt_event = type("hoge", (object,), {
        "code": 28,
        "value": 0,
    })
    bt_selfie._key_event(bt_event)

    target_func.assert_called_once_with(bt_event)


def test_key_event_any_func(mocker, bt_selfie):
    bt_event = type("hoge", (object,), {
        "code": 28,
        "value": 0,
    })
    bt_selfie._key_event(bt_event)
