# WhatsApp BCC Sender Build Instructions

This project is configured to be built with PyInstaller (pyinstaller==6.17.0).

## Prerequisites

1. Python 3.x installed.
2. Virtual environment set up and activated.
3. Dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

## Building the Executable

Run the build script:

```bash
python build_exe.py
```

this will prompt ou with two choices either the CLI mode or the GUI

## Running the Application

**IMPORTANT:** The application depends on the `attach` folder on CLI mode for configuration files (message.txt, phone_numbers.txt) and assets (images, PDFs).

1. Copy the `dist/WhatsAppSender.exe` or the  `dist/WhatsAppSenderCLI.exe (with the attach folder)` or the  to a desired location.
2. Run the executable.

Structure should look like this on CLI:

```
MyFolder/
├── WhatsAppSender_new.exe
└── attach/
    ├── images/
    ├── pdf/
    ├── message.txt
    └── phone_numbers.txt
```

---

# END.
