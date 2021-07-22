import pytest
from bt_button import SmartPalette, SmartPaletteButton, DeviceNotFoundError
from bt_button.buttons.smart_palette import _button_to_data

import pygatt


@pytest.fixture
def smart_palette(mocker):
    mocker.patch('pygatt.GATTToolBackend')
    return SmartPalette("00:00:00:00:00:00")


def test_is_connected_0(mocker, smart_palette):
    mock = mocker.Mock()
    smart_palette.device = mock
    assert smart_palette.is_connected()


def test_is_connected_1(mocker, smart_palette):
    assert not smart_palette.is_connected()


def test_connect_0(mocker, smart_palette):
    adapter_mock = mocker.patch.object(smart_palette.adapter, 'connect')

    smart_palette.connect()

    adapter_mock.assert_called_once()


def test_connect_1(mocker, smart_palette):
    adapter_mock = mocker.patch.object(
        smart_palette.adapter, 'connect',
        side_effect=pygatt.exceptions.NotConnectedError)

    with pytest.raises(DeviceNotFoundError):
        smart_palette.connect()

    adapter_mock.assert_called_once()


def test_disconnect_0(mocker, smart_palette):
    smart_palette.device = mocker.Mock()
    device_mock = mocker.patch.object(smart_palette.device, 'disconnect')

    smart_palette.disconnect()

    device_mock.assert_called_once()


def test_disconnect_1(mocker, smart_palette):
    is_connected_mock = mocker.patch.object(smart_palette, 'is_connected')
    is_connected_mock.return_value = False

    smart_palette.device = mocker.Mock()
    device_mock = mocker.patch.object(smart_palette.device, 'disconnect')

    smart_palette.disconnect()

    device_mock.assert_not_called()


@pytest.mark.parametrize("target_button", list(SmartPaletteButton))
def test_attach_pushed_listener_0(mocker, smart_palette, target_button):
    func = mocker.Mock()

    smart_palette.attach_pushed_listener(target_button, func)
    assert smart_palette.pushed_funcs[target_button] == func

    for other_button in list(SmartPaletteButton):
        if other_button != target_button:
            assert smart_palette.pushed_funcs[other_button] is None


def test_attach_pushed_listener_1(mocker, smart_palette):
    for button in list(SmartPaletteButton):
        assert smart_palette.pushed_funcs[button] is None


@pytest.mark.parametrize("target_button", list(SmartPaletteButton))
def test_detach_pushed_listener_0(mocker, smart_palette, target_button):
    func = mocker.Mock()

    for button in list(SmartPaletteButton):
        smart_palette.attach_pushed_listener(button, func)

    smart_palette.detach_pushed_listener(target_button)

    assert smart_palette.pushed_funcs[target_button] is None

    for other_button in list(SmartPaletteButton):
        if other_button != target_button:
            assert smart_palette.pushed_funcs[other_button] == func


@pytest.mark.parametrize("target_button", list(SmartPaletteButton))
def test_event_call_only_target_func(mocker, smart_palette, target_button):
    correct_func = mocker.Mock()
    mistake_func = mocker.Mock()

    for b in list(SmartPaletteButton):
        if b == target_button:
            smart_palette.attach_pushed_listener(b, correct_func)
        else:
            smart_palette.attach_pushed_listener(b, mistake_func)

    data = _button_to_data(target_button)
    smart_palette._event(0xb, data)

    correct_func.assert_called_once()
    mistake_func.assert_not_called()


@pytest.mark.parametrize("target_button", list(SmartPaletteButton))
def test_event_with_any_func(mocker, smart_palette, target_button):
    data = _button_to_data(target_button)
    smart_palette._event(0xb, data)
