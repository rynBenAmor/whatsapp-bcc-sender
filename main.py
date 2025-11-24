import sys
import pywhatkit.whats as pwk
from src.extras.pdf import sendwhatspdf
from src.extras.safety import is_installed, webbrowser_exists, read_file_safe, attach_exists
from src.extras.settings import WHATS_MAX_CAPTION, WHATS_MAX_MESSAGE, WAIT_TIME


def print_menu():
    print("\n" + "="*30)
    print("      WhatsApp Sender")
    print("="*30)
    print("1. Send simple message")
    print("2. Send images")
    print("3. Send PDF")
    print("4. Check system readiness")
    print("0. Exit")
    print()

def get_phone_numbers():
    content = read_file_safe("attach/phone_numbers.txt", default="")
    if not content:
        print("No phone numbers found in attach/phone_numbers.txt")
        return []
    return [ph for ph in content.split('\n') if ph.strip().startswith("+")]

def get_message(cap = WHATS_MAX_MESSAGE):
    msg = read_file_safe("attach/message.txt", default="")
    if not msg:
        print("No message found in attach/message.txt")
        return ""
    return msg.strip()[:cap] # max cap of a regular message

def send_simple_message():
    phone_numbers = get_phone_numbers()
    if not phone_numbers:
        return

    message = get_message()
    if not message:
        return

    for ph in phone_numbers:
        print(f"Processing {ph}...")

        try:
            pwk.sendwhatmsg_instantly(phone_no=ph, message=message, tab_close=True, wait_time=WAIT_TIME)
            print("Message sent.")
        except Exception as e:
            print(f"Failed to send to {ph}: {e}")

def send_images():
    phone_numbers = get_phone_numbers()
    if not phone_numbers:
        return
    
    img_path = input("Enter image path (default: attach/images/sample.jpg): ").strip() or "attach/images/sample.jpg"
    caption = get_message(cap=WHATS_MAX_CAPTION)

    for ph in phone_numbers:
        print(f"Processing {ph}...")

        try:
            pwk.sendwhats_image(receiver=ph, img_path=img_path, caption=caption, tab_close=True, wait_time=WAIT_TIME)
            print("Image sent.")
        except Exception as e:
            print(f"Failed to send to {ph}: {e}")

def send_pdf():
    phone_numbers = get_phone_numbers()
    if not phone_numbers:
        return

    pdf_path = input("Enter PDF path (default: attach/pdf/sample.pdf): ").strip() or "attach/pdf/sample.pdf"
    caption = get_message(cap=WHATS_MAX_CAPTION)

    for ph in phone_numbers:
        print(f"Processing {ph}...")
        try:
            sendwhatspdf(receiver=ph, pdf_path=pdf_path, caption=caption, tab_close=True, wait_time=WAIT_TIME)
            print("PDF sent.")
        except Exception as e:
            print(f"Failed to send to {ph}: {e}")

def check_system():
    print(f"PyWhatKit installed: {is_installed('pywhatkit')}")
    print(f"Webbrowser available: {webbrowser_exists()}")
    print(f"attach dir: {attach_exists()}")



def main():
    try:
        while True:
            print_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                send_simple_message()
            elif choice == "2":
                send_images()
            elif choice == "3":
                send_pdf()
            elif choice == "4":
                check_system()
            elif choice == "0":
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid option, please try again.")

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit()

if __name__ == "__main__":
    main()


