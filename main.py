import sys
from src.extras.safety import is_installed, webbrowser_exists, attach_exists
#from src.gui import run_gui
from src.core import send_simple_message, send_image, send_pdf
# ? ==================== end of imports ======================================================


def print_menu():
    print("\n" + "="*30)
    print("      WhatsApp Sender")
    print("="*30)
    print("1. Send simple message")
    print("2. Send image")
    print("3. Send PDF")
    print("4. Check system readiness")
    print("0. Exit")
    print()


def check_system():
    print(f"PyWhatKit installed: {is_installed('pywhatkit')}")
    print(f"Webbrowser available: {webbrowser_exists()}")
    print(f"attach dir: {attach_exists()}")


def main():
    try:
        """         
        mode = input("Select mode: (1) CLI, (2) GUI: ").strip()
                if mode == "2":
                    run_gui()
                    return 
        """

        while True:
            print_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                send_simple_message()
            elif choice == "2":
                send_image()
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


