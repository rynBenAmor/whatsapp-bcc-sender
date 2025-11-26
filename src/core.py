import pywhatkit.whats as pwk
from .extras.pdf import sendwhatspdf
from .extras.safety import read_file_safe, validate_phone_number, validate_file_path, random_sleep
from .extras.settings import WHATS_MAX_CAPTION, WHATS_MAX_MESSAGE, WAIT_TIME, TAB_CLOSE



def get_phone_numbers():
    content = read_file_safe("attach/phone_numbers.txt")
    if not content:
        print("Error: No phone numbers found in attach/phone_numbers.txt")
        return []
    valid_numbers = []
    for ph in content.split('\n'):
        ph = ph.strip()
        if not ph: continue
        
        valid_ph = validate_phone_number(ph)
        if valid_ph:
            valid_numbers.append(valid_ph)
        else:
            print(f"Skipping invalid phone number: {ph}")
            
    return valid_numbers


def get_message(cap = WHATS_MAX_MESSAGE):
    msg = read_file_safe("attach/message.txt")
    if not msg:
        print("No message found in attach/message.txt")
        return ""
    return msg.strip()[:cap] # max cap of a regular message


def send_simple_message(phone_numbers=None, message=None):
    if phone_numbers is None:
        phone_numbers = get_phone_numbers()
    if not phone_numbers:
        return

    if message is None:
        message = get_message()
    if not message:
        return

    for i, ph in enumerate(phone_numbers):
        if i > 0:
            random_sleep()
            
        print(f"Processing {ph}...")

        try:
            pwk.sendwhatmsg_instantly(phone_no=ph, message=message, tab_close=TAB_CLOSE, wait_time=WAIT_TIME)
            print("Message sent.")
        except Exception as e:
            print(f"Failed to send to {ph}: {e}")


def send_image(phone_numbers=None, img_path=None, caption=None):
    if phone_numbers is None:
        phone_numbers = get_phone_numbers()
    if not phone_numbers:
        return
    
    if img_path is None:
        img_path = input("Enter image path (default: attach/images/sample.jpg): ").strip() or "attach/images/sample.jpg"
    
    if not validate_file_path(img_path):
        print(f"Error: Image file not found at {img_path}")
        return

    if caption is None:
        caption = get_message(cap=WHATS_MAX_CAPTION)

    for i, ph in enumerate(phone_numbers):
        if i > 0:
            random_sleep()

        print(f"Processing {ph}...")

        try:
            pwk.sendwhats_image(receiver=ph, img_path=img_path, caption=caption, tab_close=TAB_CLOSE, wait_time=WAIT_TIME+5)
            random_sleep()
            print("Image sent.")
        except Exception as e:
            print(f"Failed to send to {ph}: {e}")


def send_pdf(phone_numbers=None, pdf_path=None, caption=None):
    if phone_numbers is None:
        phone_numbers = get_phone_numbers()
    if not phone_numbers:
        return

    if pdf_path is None:
        pdf_path = input("Enter PDF path (default: attach/pdf/sample.pdf): ").strip() or "attach/pdf/sample.pdf"
    
    if not validate_file_path(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return

    if caption is None:
        caption = get_message(cap=WHATS_MAX_CAPTION)

    for i, ph in enumerate(phone_numbers):
        if i > 0:
            random_sleep()
            
        print(f"Processing {ph}...")
        try:
            sendwhatspdf(receiver=ph, pdf_path=pdf_path, caption=caption, tab_close=TAB_CLOSE, wait_time=WAIT_TIME)
            random_sleep() # to ensure it uploads it
            print("PDF sent.")
        except Exception as e:
            print(f"Failed to send to {ph}: {e}")
