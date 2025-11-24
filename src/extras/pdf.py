import time
import os
from urllib.parse import quote

import pyautogui as pg
import webbrowser as web

from .utils import image_locate
# ? ==================== end of imports ======================================================


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
attach_img = os.path.join(BASE_DIR, "identifiers", "attach-icon.png")
#document_img = os.path.join(BASE_DIR, "identifiers", "document-icon.jpeg") # not needed for now as arrow down does the job

# ? ==================== end of constants ======================================================



"""
Press Tab enough times to reach the attachment menu.

Press Enter to open it.

Arrow down to Document.

Press Enter to open the file picker.
"""
def sendwhatspdf(
    receiver: str,
    pdf_path: str,
    caption: str = "",
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 3,
):
    web.open(f"https://web.whatsapp.com/send?phone={receiver}&text={quote(caption)}")
    time.sleep(wait_time)

    attach_btn = image_locate(attach_img)
    if attach_btn:
        pg.click(attach_btn)
        time.sleep(0.7)
        pg.press('down')
        pg.press('enter')

    else:
        print("ERROR! could not find attachment button ")

    time.sleep(2)

    pdf_abs_path = os.path.abspath(pdf_path)
    pdf_abs_path = os.path.normpath(pdf_abs_path)
    print(pdf_abs_path) 

    # * Copy path to clipboard and paste (more reliable than pg.typewrite for paths with ":" and backslashes)
    try:
        import pyperclip
        pyperclip.copy(pdf_abs_path)
    except Exception:
        from tkinter import Tk
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(pdf_abs_path)
        r.update()
        r.destroy()

    pg.hotkey('ctrl', 'v')
    pg.press('enter')

    
    time.sleep(3)
    pg.press('enter')

    if tab_close:
        time.sleep(close_time)

        pg.hotkey('ctrl', 'w')
