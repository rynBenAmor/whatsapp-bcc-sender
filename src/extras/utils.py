import os
import pyautogui as pg
# ? ==================== end of imports ======================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ? ==================== end of constants ======================================================



def image_locate(img_path: str, tries=(0.9,0.8,0.75,0.7,0.65), grayscale_opts=(False, True)):
    # saves a full screenshot and tries several confidence/grayscale combos, prints results
    full_shot = os.path.join(BASE_DIR, ".bin/debug_full.png")
    pg.screenshot(full_shot)

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