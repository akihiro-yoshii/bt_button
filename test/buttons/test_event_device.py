import pytest
import evdev

from bt_button.buttons._event_device import EventDevice, DeviceNotFoundError
from bt_button.buttons._event_device import connected_paths
from bt_button.buttons._event_device import _search_device, open_device, \
    remove_device


def test_search_device_found(mocker):
    dev_list_mock = [mocker.Mock(), ]

    list_device_mock = mocker.patch(
        "evdev.util.list_devices",
        return_value=dev_list_mock
    )

    target_object = mocker.Mock()
    target_object.name = mocker.Mock()
    target_object.uniq = mocker.Mock()

    input_device_mock = mocker.patch(
        "evdev.InputDevice",
        return_value=target_object)

    ret = _search_device(target_object.name, target_object.uniq)

    list_device_mock.assert_called_once()
    input_device_mock.assert_called_once()
    assert ret == target_object


def test_search_device_not_found(mocker):
    dev_list_mock = [mocker.Mock(), ]

    list_device_mock = mocker.patch(
        "evdev.util.list_devices",
        return_value=dev_list_mock
    )

    target_object = mocker.Mock()
    target_object.name = mocker.Mock()
    target_object.uniq = mocker.Mock()

    input_device_mock = mocker.patch(
        "evdev.InputDevice",
        return_value=target_object)

    mock_name = mocker.Mock()
    mock_uniq = mocker.Mock()

    ret = _search_device(mock_name, mock_uniq)

    list_device_mock.assert_called_once()
    input_device_mock.assert_called_once()
    assert ret is None


def test_search_device_duplicate(mocker):
    dev_path_mock = mocker.Mock()
    dev_list_mock = [dev_path_mock, ]
    connected_paths.append(dev_path_mock)

    list_device_mock = mocker.patch(
        "evdev.util.list_devices",
        return_value=dev_list_mock
    )

    target_object = mocker.Mock()
    target_object.name = mocker.Mock()
    target_object.uniq = mocker.Mock()

    input_device_mock = mocker.patch(
        "evdev.InputDevice",
        return_value=target_object)

    mock_name = mocker.Mock()
    mock_uniq = mocker.Mock()

    ret = _search_device(mock_name, mock_uniq)

    list_device_mock.assert_called_once()
    input_device_mock.assert_not_called()
    assert ret is None

    connected_paths.clear()


def test_open_device_correct(mocker):
    target_object = mocker.Mock()
    search_mock = mocker.patch(
        "bt_button.buttons._event_device._search_device",
        return_value=target_object)

    mock_name = mocker.Mock()
    mock_mac_addr = mocker.Mock()

    ret = open_device(mock_name, mock_mac_addr)

    search_mock.assert_called_once_with(mock_name, mock_mac_addr.lower())
    assert len(connected_paths) == 1
    assert ret == target_object

    connected_paths.clear()


def test_open_device_not_found(mocker):
    search_mock = mocker.patch(
        "bt_button.buttons._event_device._search_device",
        return_value=None)

    mock_name = mocker.Mock()
    mock_mac_addr = mocker.Mock()

    with pytest.raises(DeviceNotFoundError):
        open_device(mock_name, mock_mac_addr)

    search_mock.assert_called_once_with(mock_name, mock_mac_addr.lower())
    assert len(connected_paths) == 0

    connected_paths.clear()


def test_remove_device(mocker):
    path = mocker.Mock()
    connected_paths.append(path)

    remove_device(path)
    assert len(connected_paths) == 0


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
