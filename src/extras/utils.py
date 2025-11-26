import os
import pyautogui as pg
import sys

# ? ==================== end of imports ======================================================

def get_app_root():
    """Returns the root directory of the application."""
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app 
        # path into variable _MEIPASS.
        # However, for external files like 'attach', we want the directory
        # where the executable is located, not the temporary _MEIPASS.
        return os.path.dirname(sys.executable)
    else:
        # If running as a script, return the project root (2 levels up from this file)
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_DIR = get_app_root()
# ? ==================== end of constants ======================================================


def image_locate(img_path: str, tries=(0.9,0.8,0.75,0.7,0.65), grayscale_opts=(False, True)):
    # saves a full screenshot and tries several confidence/grayscale combos, prints results
    debug_dir = os.path.join(BASE_DIR, ".bin")
    if not os.path.exists(debug_dir):
        try:
            os.makedirs(debug_dir)
        except OSError:
            # If we can't create the directory (e.g. permission denied in Program Files),
            # try using temp directory or just skip saving screenshot?
            # For now, let's try to proceed without saving if it fails, or just let it fail.
            # But better to just print warning.
            print(f"Warning: Could not create debug directory {debug_dir}")
            # If we can't create dir, we can't save screenshot.
            # But the function continues to locate.
            pass

    full_shot = os.path.join(debug_dir, "debug_full.png")
    try:
        pg.screenshot(full_shot)
    except Exception as e:
        print(f"Warning: Could not save debug screenshot: {e}")

    for g in grayscale_opts:
        for c in tries:
            try:
                loc = pg.locateCenterOnScreen(img_path, confidence=c, grayscale=g)
            except Exception as e:
                print(f"locateCenterOnScreen raised: {e} (confidence={c}, grayscale={g})")
                loc = None
            print(f"try confidence={c}, grayscale={g} ->", "FOUND" if loc else "NOT FOUND")
            if loc:
                return loc
    return None