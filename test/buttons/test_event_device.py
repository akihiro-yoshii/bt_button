import pytest
import evdev

from bt_button.buttons._event_device import EventDevice


@pytest.fixture
def event_device(mocker):
    return EventDevice("00:00:00:00:00:00", "TEST")


def test_is_monitoring_0(mocker, event_device):
    event_device.device = mocker.Mock()
    assert event_device.is_monitoring()


def test_is_monitoring_1(mocker, event_device):
    assert not event_device.is_monitoring()


def test_start_monitor_0(mocker, event_device):
    open_device_mock = mocker.patch(
        "bt_button.buttons._event_device.open_device")

    event_device.start_monitor()

    open_device_mock.assert_called_once()


# def test_connect_1(mocker, bt_selfie):
#     open_device_mock = mocker.patch(
#         "bt_button.buttons._event_device.open_device")
#     open_device_mock.side_effect = DeviceNotFoundError(
#         "hoge", bt_selfie.name, bt_selfie.mac_addr)

#     with pytest.raises(DeviceNotFoundError):
#         bt_selfie.connect()

#     open_device_mock.assert_called_once()


def test_finish_monitor(mocker, event_device):
    event_device.device = mocker.Mock()
    event_device.device.path = mocker.Mock()

    open_device_mock = mocker.patch(
        "bt_button.buttons._event_device.remove_device")

    event_device._finish_monitor()

    open_device_mock.assert_called_once()


def test_run_0(mocker, event_device):
    target_func = mocker.Mock()
    event_device._key_event = target_func

    event_mock = type("hoge", (object,), {
        "type": evdev.events.EV_KEY,
    })
    event_device.device = mocker.Mock()
    mocker.patch.object(
        event_device.device, 'read_loop', return_value=[event_mock, ])

    event_device._run()

    target_func.assert_called_once_with(event_mock)


def test_run_1(mocker, event_device):
    target_func = mocker.Mock()
    event_device._key_event = target_func

    event_mock = type("hoge", (object,), {
        "type": mocker.Mock()
    })
    event_device.device = mocker.Mock()
    mocker.patch.object(
        event_device.device, 'read_loop', return_value=[event_mock, ])

    event_device._run()

    target_func.assert_not_called()


def test_run_throw_OSError(mocker, event_device):
    finish_monitor = mocker.Mock()
    event_device._finish_monitor = finish_monitor

    event_device.device = mocker.Mock()
    mocker.patch.object(event_device.device, 'read_loop', side_effect=OSError)

    event_device._run()

    finish_monitor.assert_called_once()


def test_coverage_0(mocker, event_device):
    open_device_mock = mocker.patch(
        "bt_button.buttons._event_device.open_device")

    event_device.connect()
    event_device.is_connected()

    open_device_mock.assert_called_once()
