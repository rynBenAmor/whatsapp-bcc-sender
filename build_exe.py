import PyInstaller.__main__


def build():
    
    # * base build options
    options = [
        '--onefile',                # Create a single executable
        '--clean',                  # Clean cache
        
        # Hidden imports often needed for these libraries
        '--hidden-import=tkinter',
        '--hidden-import=pywhatkit',
        '--hidden-import=PIL',      # Pillow (used by pyautogui/pywhatkit)
        
        # Add data files
        '--add-data=src/extras/identifiers;src/extras/identifiers',
    ]

    # * CLI or GUI(preferred)
    print("press 1 for CLI build or 2 for GUI build")
    mode = input("Enter mode: ").strip()
    
    if mode == "2":
        options.append("src/gui.py")
        options.append("--name=WhatsAppSender")
        options.append("--windowed")
    elif mode == "1":
        options.append("main.py")
        options.append("--name=WhatsAppSenderCLI")
        options.append("--console")
    else:
        print("Invalid mode, please try again.")
        return
    
    print("Building WhatsAppSender...")    

    # Run PyInstaller
    PyInstaller.__main__.run(options)
    
    print("Build complete.")
    print("Executable is in the 'dist' folder.")
    print("CLI mode note: Make sure to copy the 'attach' folder to the same directory as the executable before running it.")

if __name__ == '__main__':
    build()
