# WhatsApp Blid-Carbon-Copy Messaging

## Goal:

I need a way to send WhatsApp messages in a **blind carbon copy (BCC)** style similar to Gmail so that clients receive messages individually without seeing each other’s numbers.

## Tech Stack:

* PyWhatKit : simple automation for WhatsApp Web based on PyAutoGUI (not selenium)
* **PyAutoGUI (custom scripts)** : added an extra module to full fill my automation needs
* **Wrapper Layer** : lightweight abstraction to tie everything together and simulate BCC-style messaging in a CLI and maybe a standalone executable file
