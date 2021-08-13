import pytest
import evdev
from bt_button import BTselfie, BtSelfieButton, BtSelfieButtonEvent
from bt_button import DeviceNotFoundError
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
        "bt_button.buttons._event_device.open_device")

    bt_selfie.connect()

    open_device_mock.assert_called_once()


def test_connect_1(mocker, bt_selfie):
    open_device_mock = mocker.patch(
        "bt_button.buttons._event_device.open_device")
    open_device_mock.side_effect = DeviceNotFoundError(
        "hoge", bt_selfie.name, bt_selfie.mac_addr)

    with pytest.raises(DeviceNotFoundError):
        bt_selfie.connect()

    open_device_mock.assert_called_once()


@pytest.mark.parametrize("button", list(BtSelfieButton))
@pytest.mark.parametrize("event", list(BtSelfieButtonEvent))
def test_attach_clicked_listener_0(mocker, bt_selfie, button, event):
    func = mocker.Mock()
    for b in list(BtSelfieButton):
        for e in list(BtSelfieButtonEvent):
            bt_selfie.attach_button_event_listener(button, event, func)

    assert bt_selfie.button_event_funcs[button][event] == func


def test_attach_button_event_listener_1(mocker, bt_selfie):
    for b in list(BtSelfieButton):
        for e in list(BtSelfieButtonEvent):
            assert bt_selfie.button_event_funcs[b][e] is None


@pytest.mark.parametrize("button", list(BtSelfieButton))
@pytest.mark.parametrize("event", list(BtSelfieButtonEvent))
def test_detach_button_event_listener_0(mocker, bt_selfie, button, event):
    func = mocker.Mock()

    for b in list(BtSelfieButton):
        for e in list(BtSelfieButtonEvent):
            bt_selfie.attach_button_event_listener(b, e, func)

    bt_selfie.detach_button_event_listener(button, event)
    assert bt_selfie.button_event_funcs[button][event] is None

    for b in list(BtSelfieButton):
        for e in list(BtSelfieButtonEvent):
            if not (b == button and e == event):
                assert bt_selfie.button_event_funcs[b][e] == func


@pytest.mark.parametrize("button", list(BtSelfieButton))
@pytest.mark.parametrize("event", list(BtSelfieButtonEvent))
def test_run_0(mocker, bt_selfie, button, event):
    event_mock = type("hoge", (object,), {
        "type": evdev.events.EV_KEY,
        "code": button,
        "value": event,
    })

    bt_selfie.device = mocker.Mock()
    mocker.patch.object(
        bt_selfie.device, 'read_loop', return_value=[event_mock, ])

    target_func = mocker.Mock()
    bt_selfie.attach_button_event_listener(button, event, target_func)

    bt_selfie._run()

    target_func.assert_called_once_with(event_mock)


@pytest.mark.parametrize("button", list(BtSelfieButton))
@pytest.mark.parametrize("event", list(BtSelfieButtonEvent))
def test_run_1(mocker, bt_selfie, button, event):
    mocker.patch("bt_button.buttons._event_device.remove_device")

    bt_selfie.device = mocker.Mock()
    mocker.patch.object(bt_selfie.device, 'read_loop', side_effect=OSError)

    target_func = mocker.Mock()
    bt_selfie.attach_button_event_listener(button, event, target_func)

    bt_selfie._run()

    target_func.assert_not_called()


@pytest.mark.parametrize("button", list(BtSelfieButton))
@pytest.mark.parametrize("event", list(BtSelfieButtonEvent))
def test_run_2(mocker, bt_selfie, button, event):
    event_mock = type("hoge", (object,), {
        "type": mocker.Mock()
    })

    bt_selfie.device = mocker.Mock()
    mocker.patch.object(
        bt_selfie.device, 'read_loop', return_value=[event_mock, ])

    target_func = mocker.Mock()
    bt_selfie.attach_button_event_listener(button, event, target_func)

    bt_selfie._run()

    target_func.assert_not_called()


@pytest.mark.parametrize("button", list(BtSelfieButton))
@pytest.mark.parametrize("event", list(BtSelfieButtonEvent))
def test_key_event_call_only_target_func(mocker, bt_selfie, button, event):
    correct_func = mocker.Mock()
    mistake_func = mocker.Mock()

    for b in list(BtSelfieButton):
        for e in list(BtSelfieButtonEvent):
            if b == button and e == event:
                bt_selfie.attach_button_event_listener(b, e, correct_func)
            else:
                bt_selfie.attach_button_event_listener(b, e, mistake_func)

    bt_event = type("hoge", (object,), {
        "code": button,
        "value": event,
    })
    bt_selfie._key_event(bt_event)

    correct_func.assert_called_once_with(bt_event)
    mistake_func.assert_not_called()


@pytest.mark.parametrize("button", list(BtSelfieButton))
@pytest.mark.parametrize("event", list(BtSelfieButtonEvent))
def test_key_event_with_any_func(bt_selfie, button, event):

    event = type("hoge", (object,), {
        "code": button,
        "value": event,
    })
    bt_selfie._key_event(event)
