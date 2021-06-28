import pytest
from bt_button import SmartPalette, SmartPaletteButton


@pytest.fixture
def smart_palette(mocker):
    return SmartPalette("00:00:00:00:00:00")


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