import os
import importlib.util
import webbrowser
from typing import Union, Optional
# ? ==================== end of imports ======================================================



# * startup checkers
def is_installed(package_name):
    return importlib.util.find_spec(package_name) is not None


def webbrowser_exists()-> bool:
    try:
        webbrowser.get()
    except:
        print("Error: No browser available")
        return False

    return True


def attach_exists() -> bool:
    folder_name = "attach"
    if not os.path.exists(folder_name):
        print(f"Warning: '{folder_name}' folder not found.")
        return False
    if not os.path.isdir(folder_name):
        print(f"Warning: '{folder_name}' is not a directory.")
        return False
    if not os.listdir(folder_name):
        print(f"Warning: '{folder_name}' folder is empty.")
        return False
    #check if pdf, images, message.txt exists
    required_files = [
        os.path.join(folder_name, "pdf"),
        os.path.join(folder_name, "images"),
        os.path.join(folder_name, "message.txt")
    ]
    for path in required_files:
        if not os.path.exists(path):
            print(f"Warning: Required path '{path}' not found in '{folder_name}' folder.")
            return False

    return True



# * safety parsers
def read_file_safe(
        file_path: str,
        mode: str = "r",
        encoding: str = "utf-8",
        default: Optional[Union[str, bytes]] = None
    ) -> Optional[Union[str, bytes]]:
    """
    Utility function to safely read a file.

    Args:
        path (str): Path to the file.
        mode (str): File mode, default "r".
        encoding (str): Encoding for text files.
        default (Any): Value to return if file is missing or unreadable.

    Returns:
        str or Any: File contents if successful, else `default`.
    
    Usage:
        read_file_safe("message.txt", default="No message found")
    """
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found.")
        return default

    try:
        with open(file_path, mode, encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return default


