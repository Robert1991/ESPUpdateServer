from unittest.mock import patch
import pytest
from node_mcu_update_server import update_manager


def test_version_string_is_valid():
    assert not update_manager.version_string_is_valid("foo")
    assert not update_manager.version_string_is_valid("123")
    assert not update_manager.version_string_is_valid("12.3")
    assert not update_manager.version_string_is_valid("12..3")
    assert update_manager.version_string_is_valid("12.1.3-10")
    assert update_manager.version_string_is_valid("0.11.0-22")


def test_device_version_string_is_valid():
    assert not update_manager.device_version_string_is_valid("ABCDfoo")
    assert not update_manager.device_version_string_is_valid("ABCD.123")
    assert not update_manager.device_version_string_is_valid("ABCD-0.12.3")
    assert not update_manager.device_version_string_is_valid("12..3-ABCD")
    assert update_manager.device_version_string_is_valid("ABCDEF-12.1.3-1")
    assert update_manager.device_version_string_is_valid("ABCDEF-12.1.3-1000")


def test_stored_version_is_higher_when_its_not_first_digit():
    assert not update_manager.version_is_higher("0.0.0", "1.0.0")


def test_stored_version_is_equal_when_its_not():
    assert not update_manager.version_is_equal("0.0.0", "1.0.0")


def test_stored_version_is_equal():
    assert update_manager.version_is_equal("0.0.0", "0.0.0")


def test_stored_version_is_higher_when_its_not_second_digit():
    assert not update_manager.version_is_higher("0.0.0", "0.1.0")


def test_stored_version_is_higher_when_its_not_third_digit():
    assert not update_manager.version_is_higher("1.1.0", "1.1.1")


def test_stored_version_is_higher_when_its_not_cross_digit():
    assert not update_manager.version_is_higher("0.9.0", "1.0.0")


def test_stored_version_is_higher_when_equal():
    assert not update_manager.version_is_higher("1.1.1", "1.1.1")


def test_stored_version_is_higher_when_it_is():
    assert update_manager.version_is_higher("2.1.0", "1.1.1")


def test_no_update_when_device_folder_not_exists():
    def update_folder_path_check_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return False
        raise Exception("not expected arg: " + update_folder_path)

    with patch('os.path.exists', update_folder_path_check_mock):
        assert not update_manager.update_exists("ABCDEF-0.10.0-10")


def test_no_update_when_device_folder_exists_but_no_updates():
    def update_folder_path_check_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return True
        raise Exception("not expected arg: " + update_folder_path)

    def list_update_folder_files_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return []
        raise Exception("not expected arg: " + update_folder_path)
    with patch('os.path.exists', update_folder_path_check_mock):
        with patch('os.listdir', list_update_folder_files_mock):
            assert not update_manager.update_exists("ABCDEF-0.10.0-10")


def test_no_update_when_device_folder_exists_no_updates_but_other_files():
    def update_folder_path_check_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return True
        raise Exception("not expected arg: " + update_folder_path)

    def list_update_folder_files_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return ["test.bin", "0.10.1-11.txt"]
        raise Exception("not expected arg: " + update_folder_path)
    with patch('os.path.exists', update_folder_path_check_mock):
        with patch('os.listdir', list_update_folder_files_mock):
            assert not update_manager.update_exists("ABCDEF-0.10.0-12")


def test_no_update_when_device_folder_exists_only_older_updates():
    def update_folder_path_check_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return True
        raise Exception("not expected arg: " + update_folder_path)

    def list_update_folder_files_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return ["0.10.0-9.bin", "0.9.0-20.bin"]
        raise Exception("not expected arg: " + update_folder_path)
    with patch('os.path.exists', update_folder_path_check_mock):
        with patch('os.listdir', list_update_folder_files_mock):
            assert not update_manager.update_exists("ABCDEF-0.10.0-10")


def test_update_exists_only_lower():
    def update_folder_path_check_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return True
        raise Exception("not expected arg: " + update_folder_path)

    def list_update_folder_files_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return ["0.10.0-10.bin", "0.10.0-9.bin", "0.10.0-8.bin"]
        raise Exception("not expected arg: " + update_folder_path)
    with patch('os.path.exists', update_folder_path_check_mock):
        with patch('os.listdir', list_update_folder_files_mock):
            assert not update_manager.update_exists("ABCDEF-0.10.0-10")

def test_update_exists():
    def update_folder_path_check_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return True
        raise Exception("not expected arg: " + update_folder_path)

    def list_update_folder_files_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return ["0.10.0-11.bin", "0.10.0-10.bin", "0.9.0-5.bin"]
        raise Exception("not expected arg: " + update_folder_path)
    with patch('os.path.exists', update_folder_path_check_mock):
        with patch('os.listdir', list_update_folder_files_mock):
            assert update_manager.update_exists("ABCDEF-0.10.0-10")


def test_update_exists_higher_version_number():
    def update_folder_path_check_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return True
        raise Exception("not expected arg: " + update_folder_path)

    def list_update_folder_files_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return ["0.10.0-0.bin", "0.9.0-5.bin"]
        raise Exception("not expected arg: " + update_folder_path)
    with patch('os.path.exists', update_folder_path_check_mock):
        with patch('os.listdir', list_update_folder_files_mock):
            assert update_manager.update_exists("ABCDEF-0.9.0-10")


def test_update_exists_higher_build_number():
    def update_folder_path_check_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return True
        raise Exception("not expected arg: " + update_folder_path)

    def list_update_folder_files_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return ["0.10.0-1.bin", "0.9.0-5.bin"]
        raise Exception("not expected arg: " + update_folder_path)
    with patch('os.path.exists', update_folder_path_check_mock):
        with patch('os.listdir', list_update_folder_files_mock):
            assert update_manager.update_exists("ABCDEF-0.10.0-0")

def test_get_next_update_path():
    def update_folder_path_check_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return True
        raise Exception("not expected arg: " + update_folder_path)

    def list_update_folder_files_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return ["0.11.0-10.bin", "1.0.0-0.bin", "0.9.0-20.bin"]
        raise Exception("not expected arg: " + update_folder_path)
    with patch('os.path.exists', update_folder_path_check_mock):
        with patch('os.listdir', list_update_folder_files_mock):
            assert update_manager.get_next_update_path("ABCDEF-0.10.0-11") \
                == "updates/ABCDEF/1.0.0-0.bin"


def test_get_next_update_path_2():
    def update_folder_path_check_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return True
        raise Exception("not expected arg: " + update_folder_path)

    def list_update_folder_files_mock(update_folder_path):
        if update_folder_path == "updates/ABCDEF":
            return ["0.10.0-11.bin", "0.10.0-9.bin", "0.10.0-8.bin"]
        raise Exception("not expected arg: " + update_folder_path)
    with patch('os.path.exists', update_folder_path_check_mock):
        with patch('os.listdir', list_update_folder_files_mock):
            assert update_manager.get_next_update_path("ABCDEF-0.10.0-9") \
                == "updates/ABCDEF/0.10.0-11.bin"
