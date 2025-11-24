import importlib.util
# ? ==================== end of imports ======================================================


def is_installed(package_name):
    return importlib.util.find_spec(package_name) is not None