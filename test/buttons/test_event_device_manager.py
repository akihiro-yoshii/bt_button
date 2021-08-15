import pytest

from bt_button.buttons._event_device_manager import EventDeviceManager
from bt_button import DeviceNotFoundError


@pytest.fixture(scope="function", autouse=True)
def setup():
    EventDeviceManager.reset()


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

    ret = EventDeviceManager._search_device(
        target_object.name, target_object.uniq)

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

    ret = EventDeviceManager._search_device(mock_name, mock_uniq)

    list_device_mock.assert_called_once()
    input_device_mock.assert_called_once()
    assert ret is None


def test_search_device_duplicate(mocker):
    dev_path_mock = mocker.Mock()
    dev_list_mock = [dev_path_mock, ]
    EventDeviceManager.connected_paths.append(dev_path_mock)

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

    ret = EventDeviceManager._search_device(mock_name, mock_uniq)

    list_device_mock.assert_called_once()
    input_device_mock.assert_not_called()
    assert ret is None


def test_open_device_correct(mocker):
    target_object = mocker.Mock()
    module = "bt_button.buttons._event_device_manager"
    module += ".EventDeviceManager._search_device"
    search_mock = mocker.patch(module, return_value=target_object)

    mock_name = mocker.Mock()
    mock_mac_addr = mocker.Mock()

    ret = EventDeviceManager.open_device(mock_name, mock_mac_addr)

    search_mock.assert_called_once_with(mock_name, mock_mac_addr.lower())
    assert len(EventDeviceManager.connected_paths) == 1
    assert ret == target_object


def test_open_device_not_found(mocker):
    module = "bt_button.buttons._event_device_manager"
    module += ".EventDeviceManager._search_device"
    search_mock = mocker.patch(module, return_value=None)

    mock_name = mocker.Mock()
    mock_mac_addr = mocker.Mock()

    with pytest.raises(DeviceNotFoundError):
        EventDeviceManager.open_device(mock_name, mock_mac_addr)

    search_mock.assert_called_once_with(mock_name, mock_mac_addr.lower())
    assert len(EventDeviceManager.connected_paths) == 0


def test_remove_device(mocker):
    path = mocker.Mock()
    EventDeviceManager.connected_paths.append(path)

    EventDeviceManager.remove_device(path)
    assert len(EventDeviceManager.connected_paths) == 0


def test_reset(mocker):
    path = mocker.Mock()
    EventDeviceManager.connected_paths.append(path)

    EventDeviceManager.reset()
    assert len(EventDeviceManager.connected_paths) == 0
