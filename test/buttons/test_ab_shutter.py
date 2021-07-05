import pytest
from bt_button import AbShutter, AbShutterButton, AbShutterButtonEvent


@pytest.fixture
def ab_shutter(mocker):
    mocker.patch("bt_button.buttons._device_manager.open_device",
                 return_value=1)
    return AbShutter("00:00:00:00:00:00")


@pytest.mark.parametrize("button", list(AbShutterButton))
@pytest.mark.parametrize("event", list(AbShutterButtonEvent))
def test_attach_button_event_listener_0(mocker, ab_shutter, button, event):
    func = mocker.Mock()

    ab_shutter.attach_button_event_listener(button, event, func)
    assert ab_shutter.button_event_funcs[button][event] == func

    for b in list(AbShutterButton):
        for e in list(AbShutterButtonEvent):
            if not (b == button and e == event):
                assert ab_shutter.button_event_funcs[b][e] is None


def test_attach_button_event_listener_1(mocker, ab_shutter):
    for button in list(AbShutterButton):
        for event in list(AbShutterButtonEvent):
            assert ab_shutter.button_event_funcs[button][event] is None


@pytest.mark.parametrize("button", list(AbShutterButton))
@pytest.mark.parametrize("event", list(AbShutterButtonEvent))
def test_detach_button_event_listener_0(mocker, ab_shutter, button, event):
    func = mocker.Mock()

    for b in list(AbShutterButton):
        for e in list(AbShutterButtonEvent):
            ab_shutter.attach_button_event_listener(b, e, func)

    ab_shutter.detach_button_event_listener(button, event)
    assert ab_shutter.button_event_funcs[button][event] is None

    for b in list(AbShutterButton):
        for e in list(AbShutterButtonEvent):
            if not (b == button and e == event):
                assert ab_shutter.button_event_funcs[b][e] == func


@pytest.mark.parametrize("button", list(AbShutterButton))
@pytest.mark.parametrize("event", list(AbShutterButtonEvent))
def test_key_event_call_only_target_func(mocker, ab_shutter, button, event):
    correct_func = mocker.Mock()
    mistake_func = mocker.Mock()

    for b in list(AbShutterButton):
        for e in list(AbShutterButtonEvent):
            if b == button and e == event:
                ab_shutter.attach_button_event_listener(b, e, correct_func)
            else:
                ab_shutter.attach_button_event_listener(b, e, mistake_func)

    bt_event = type("hoge", (object,), {
        "code": button,
        "value": event,
    })
    ab_shutter._key_event(bt_event)

    correct_func.assert_called_once_with(bt_event)
    mistake_func.assert_not_called()


@pytest.mark.parametrize("button", list(AbShutterButton))
@pytest.mark.parametrize("event", list(AbShutterButtonEvent))
def test_key_event_with_any_func(ab_shutter, button, event):

    event = type("hoge", (object,), {
        "code": button,
        "value": event,
    })
    ab_shutter._key_event(event)
