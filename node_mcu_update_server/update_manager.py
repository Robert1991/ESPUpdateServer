
import os
import re

def version_is_equal(version, other_version):
    return version == other_version

def version_is_higher(version, other_version):
    version_split = version.split(".")
    other_version_split = other_version.split(".")

    if int(other_version_split[0]) > int(version_split[0]):
        return False
    else:
        if int(other_version_split[0]) == int(version_split[0]):
            if int(other_version_split[1]) > int(version_split[1]):
                return False
            else:
                if int(other_version_split[1]) == int(version_split[1]):
                    if int(other_version_split[1]) > int(version_split[1]):
                        return False
                    else:
                        return int(version_split[2]) > int(other_version_split[2])
                else:
                    return True
        else:
            return True


def version_string_is_valid(checked_version_string):
    VERSION_PATTERN = "[0-9]{1,2}\\.[0-9]{1,3}\\.[0-9]{1,4}\\-[0-9]{1,4}$"
    versionMatcher = re.compile(VERSION_PATTERN)
    return versionMatcher.match(checked_version_string)


def device_version_string_is_valid(checked_version_string):
    DEVICE_VERSION_PATTERN = "^[a-zA-Z0-9]{6}\\-[0-9]{1,2}\\.[0-9]{1,3}\\.[0-9]{1,4}\\-[0-9]{1,4}$"
    deviceVersionMatcher = re.compile(DEVICE_VERSION_PATTERN)
    return deviceVersionMatcher.match(checked_version_string)


def update_exists(version_string):
    device_id, version_number, build_number = _split_version_string(version_string)
    device_update_folder = "updates/" + device_id
    print(device_update_folder)
    for file in _list_all_updates_in(device_update_folder):
        stored_update_version_number = file.replace(".bin", "")
        stored_version_number, stored_build_number = _split_stored_version_string(stored_update_version_number)
        if version_is_higher(stored_version_number, version_number):
            print("hello1")
            return True
        elif version_is_equal(stored_version_number, version_number):
            if int(stored_build_number) > int(build_number):
                return True
    return False


def get_next_update_path(version_string):
    device_id, version_number, build_number = _split_version_string(version_string)
    device_update_folder = "updates/" + device_id

    current_highest_version = None
    current_highest_build_number = None
    for file in _list_all_updates_in(device_update_folder):
        update_version_number = file.replace(".bin", "")
        stored_version_number, stored_build_number = _split_stored_version_string(
            update_version_number)

        if current_highest_version and current_highest_build_number:
            if version_is_higher(stored_version_number, current_highest_version):
                current_highest_version = stored_version_number
                current_highest_build_number = stored_build_number
            elif version_is_equal(stored_version_number, current_highest_version):
                if int(current_highest_build_number) < int(stored_build_number):
                    current_highest_build_number = stored_build_number
        else:
            if version_is_higher(stored_version_number, version_number):
                current_highest_version = stored_version_number
                current_highest_build_number = stored_build_number
            elif version_is_equal(stored_version_number, version_number):
                if int(build_number) < int(stored_build_number):
                    current_highest_version = stored_version_number
                    current_highest_build_number = stored_build_number
    if current_highest_version:
        return "updates/" + device_id + "/" + current_highest_version + "-" + current_highest_build_number + ".bin"
    return ""


def _list_all_updates_in(device_folder):
    if os.path.exists(device_folder):
        folder_content = os.listdir(device_folder)

        return list(filter(lambda file: file.endswith(".bin") and version_string_is_valid(file.replace(".bin", "")),
                           folder_content))
    return []


def _split_stored_version_string(version_string):
    version_string_split = version_string.split("-")
    version_number = version_string_split[0]
    buildNumber = version_string_split[1]
    return version_number, buildNumber


def _split_version_string(version_string):
    version_string_split = version_string.split("-")
    device_id = version_string_split[0]
    version_number = version_string_split[1]
    buildNumber = version_string_split[2]
    return device_id, version_number, buildNumber
