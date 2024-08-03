import platform


def is_windows_10():
    os_version = platform.version()
    os_name = platform.system()
    return os_name == "Windows" and os_version.startswith("10")
