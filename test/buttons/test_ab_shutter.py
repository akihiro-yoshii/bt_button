import pytest
from bt_button import AbShutter, AbShutterButtonEvent


@pytest.fixture
def ab_shutter(mocker):
    mocker.patch("bt_button.buttons._device_manager.open_device",
                 return_value=1)
    return AbShutter("00:00:00:00:00:00")


@pytest.mark.parametrize("event", list(AbShutterButtonEvent))
def test_attach_button_event_listener_0(mocker, ab_shutter, event):
    func = mocker.Mock()

    ab_shutter.attach_button_event_listener(event, func)
    assert ab_shutter.button_event_funcs[event] == func

    for other_event in list(AbShutterButtonEvent):
        if other_event != event:
            assert ab_shutter.button_event_funcs[other_event] is None


def test_attach_button_event_listener_1(mocker, ab_shutter):
    for event in list(AbShutterButtonEvent):
        assert ab_shutter.button_event_funcs[event] is None


@pytest.mark.parametrize("event", list(AbShutterButtonEvent))
def test_detach_button_event_listener_0(mocker, ab_shutter, event):
    func = mocker.Mock()

    for e in list(AbShutterButtonEvent):
        ab_shutter.attach_button_event_listener(e, func)

    ab_shutter.detach_button_event_listener(event)
    assert ab_shutter.button_event_funcs[event] is None

    for other_event in list(AbShutterButtonEvent):
        if other_event != event:
            assert ab_shutter.button_event_funcs[other_event] == func
