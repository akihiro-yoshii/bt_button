import pytest
from bt_button.button import AbShutter


@pytest.fixture
def ab_shutter(mocker):
    mocker.patch("bt_button.button.open_device", return_value=1)
    return AbShutter("00:00:00:00:00:00")


def test_add_pushed_listener(mocker, ab_shutter):
    func = mocker.Mock()
    ab_shutter.add_pushed_listener(func)

    assert len(ab_shutter.pushed_funcs) == 1
