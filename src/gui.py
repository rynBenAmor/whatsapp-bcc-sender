import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import sys
import os
import threading
import queue

# We need to add the parent directory to sys.path to import from main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core import send_simple_message, send_image, send_pdf
from src.extras.safety import validate_phone_number, validate_file_path, read_file_safe

class WhatsAppSenderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp BCC")
        self.root.geometry("600x500")

        # Redirect stdout to the log widget
        self._log_queue = queue.Queue()
        self._orig_stdout = sys.stdout
        self._orig_stderr = sys.stderr
        self._logging_poll_interval = 100  # ms

        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Tabs
        self.create_message_tab()
        self.create_image_tab()
        self.create_pdf_tab()

        # Log Area
        self.create_log_area()

    def create_message_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Simple Message")

        # Phone numbers frame with browse button
        frame_phone = ttk.LabelFrame(tab, text="Phone Numbers", padding=10)
        frame_phone.pack(fill='x', padx=10, pady=10)

        btn_browse_msg = ttk.Button(
            frame_phone,
            text="Load from File",
            command=lambda: self.load_phone_numbers_from_file(self.txt_phone_msg)
        )
        btn_browse_msg.pack(side='top', anchor='e', pady=(0, 5))

        self.txt_phone_msg = scrolledtext.ScrolledText(frame_phone, height=4, width=50)
        self.txt_phone_msg.pack(fill='both', expand=True)

        # Message content
        ttk.Label(tab, text="Message:").pack(anchor='w', padx=10, pady=(10, 0))
        self.txt_msg_content = scrolledtext.ScrolledText(tab, height=6)
        self.txt_msg_content.pack(fill='both', expand=True, padx=10, pady=10)

        # Send button
        btn_send_msg = ttk.Button(tab, text="Send Message", command=self.on_send_message)
        btn_send_msg.pack(pady=10)

    def create_image_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Image")

        # Phone numbers frame with browse button
        frame_phone = ttk.LabelFrame(tab, text="Phone Numbers", padding=10)
        frame_phone.pack(fill='x', padx=10, pady=10)

        btn_browse_img = ttk.Button(
            frame_phone,
            text="Load from File",
            command=lambda: self.load_phone_numbers_from_file(self.txt_phone_img)
        )
        btn_browse_img.pack(side='top', anchor='e', pady=(0, 5))

        self.txt_phone_img = scrolledtext.ScrolledText(frame_phone, height=4, width=50)
        self.txt_phone_img.pack(fill='both', expand=True)

        # Image file
        frame_file = ttk.Frame(tab)
        frame_file.pack(fill='x', padx=10, pady=10)
        ttk.Label(frame_file, text="Image:").pack(side='left')
        self.entry_img_path = ttk.Entry(frame_file)
        self.entry_img_path.pack(side='left', fill='x', expand=True, padx=5)
        btn_browse = ttk.Button(
            frame_file,
            text="Browse",
            command=lambda: self.browse_file(self.entry_img_path, [("Images", ("*.jpg", "*.jpeg", "*.png"))])
        )
        btn_browse.pack(side='left')

        # Caption
        ttk.Label(tab, text="Caption:").pack(anchor='w', padx=10, pady=(10, 0))
        self.txt_caption_img = scrolledtext.ScrolledText(tab, height=4)
        self.txt_caption_img.pack(fill='both', expand=True, padx=10, pady=10)

        # Send button
        btn_send_img = ttk.Button(tab, text="Send Image", command=self.on_send_image)
        btn_send_img.pack(pady=10)

    def create_pdf_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="PDF")

        # Phone numbers frame with browse button
        frame_phone = ttk.LabelFrame(tab, text="Phone Numbers", padding=10)
        frame_phone.pack(fill='x', padx=10, pady=10)

        btn_browse_pdf = ttk.Button(
            frame_phone,
            text="Load from File",
            command=lambda: self.load_phone_numbers_from_file(self.txt_phone_pdf)
        )
        btn_browse_pdf.pack(side='top', anchor='e', pady=(0, 5))

        self.txt_phone_pdf = scrolledtext.ScrolledText(frame_phone, height=4, width=50)
        self.txt_phone_pdf.pack(fill='both', expand=True)

        # PDF file
        frame_file = ttk.Frame(tab)
        frame_file.pack(fill='x', padx=10, pady=10)
        ttk.Label(frame_file, text="PDF:").pack(side='left')
        self.entry_pdf_path = ttk.Entry(frame_file)
        self.entry_pdf_path.pack(side='left', fill='x', expand=True, padx=5)
        btn_browse = ttk.Button(
            frame_file,
            text="Browse",
            command=lambda: self.browse_file(self.entry_pdf_path, [("PDF Files", ("*.pdf",))])
        )
        btn_browse.pack(side='left')

        # Caption
        ttk.Label(tab, text="Caption:").pack(anchor='w', padx=10, pady=(10, 0))
        self.txt_caption_pdf = scrolledtext.ScrolledText(tab, height=4)
        self.txt_caption_pdf.pack(fill='both', expand=True, padx=10, pady=10)

        # Send button
        btn_send_pdf = ttk.Button(tab, text="Send PDF", command=self.on_send_pdf)
        btn_send_pdf.pack(pady=10)

    def create_log_area(self):
        lbl_log = ttk.Label(self.root, text="Logs:")
        lbl_log.pack(anchor='w', padx=10)

        self.txt_log = scrolledtext.ScrolledText(self.root, height=8, state='disabled')
        self.txt_log.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        # Redirect stdout
        sys.stdout = self
        sys.stderr = self
        # start polling the queue and ensure stdout is restored on close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.after(self._logging_poll_interval, self._poll_log_queue)

    def write(self, text):
        # called from other threads: enqueue and return quickly
        try:
            s = str(text)
        except Exception:
            s = "<non-string output>"
        self._log_queue.put(s)

    def flush(self):
        pass

    def _poll_log_queue(self):
        # run on main thread to safely update widget
        try:
            updated = False
            while True:
                s = self._log_queue.get_nowait()
                self.txt_log.configure(state='normal')
                self.txt_log.insert(tk.END, s)
                updated = True
        except queue.Empty:
            pass
        if updated:
            self.txt_log.see(tk.END)
            self.txt_log.configure(state='disabled')
            self.root.update_idletasks()
        self.root.after(self._logging_poll_interval, self._poll_log_queue)

    def _on_close(self):
        # restore stdout/stderr and quit
        sys.stdout = self._orig_stdout
        sys.stderr = self._orig_stderr
        self.root.destroy()

    def browse_file(self, entry_widget, filetypes):
        # ensure filetypes uses tuple-of-patterns for better compatibility
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, filename)

    def get_valid_numbers(self, text_widget):
        """Parse phone numbers from text widget. Supports pasted numbers or file path."""
        raw_text = text_widget.get("1.0", tk.END).strip()
        
        # If text looks like a file path, try to read it
        if raw_text.endswith('.txt') and os.path.exists(raw_text):
            try:
                raw_text = read_file_safe(raw_text, default="")
            except Exception as e:
                print(f"Warning: Could not read file '{raw_text}': {e}")
                return []
        
        valid_numbers = []
        for line in raw_text.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):  # skip empty lines and comments
                continue
            valid_ph = validate_phone_number(line)
            if valid_ph:
                valid_numbers.append(valid_ph)
            else:
                print(f"Skipped invalid phone number: {line}")
        
        return valid_numbers

    def load_phone_numbers_from_file(self, text_widget):
        """Browse and load phone numbers from a .txt file."""
        filename = filedialog.askopenfilename(
            filetypes=[("Text Files", ("*.txt",)), ("All Files", ("*",))]
        )
        if filename:
            try:
                content = read_file_safe(filename, default="")
                text_widget.delete("1.0", tk.END)
                text_widget.insert("1.0", content)
                print(f"Loaded phone numbers from: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file: {e}")

    def run_in_thread(self, target):
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()

    def on_send_message(self):
        numbers = self.get_valid_numbers(self.txt_phone_msg)
        message = self.txt_msg_content.get("1.0", tk.END).strip()

        if not numbers:
            messagebox.showerror("Error", "No valid phone numbers provided.")
            return
        if not message:
            messagebox.showerror("Error", "Message cannot be empty.")
            return

        self.run_in_thread(lambda: send_simple_message(numbers, message))

    def on_send_image(self):
        numbers = self.get_valid_numbers(self.txt_phone_img)
        img_path = self.entry_img_path.get().strip()
        caption = self.txt_caption_img.get("1.0", tk.END).strip()

        if not numbers:
            messagebox.showerror("Error", "No valid phone numbers provided.")
            return
        if not img_path or not validate_file_path(img_path):
            messagebox.showerror("Error", "Invalid image path.")
            return

        self.run_in_thread(lambda: send_image(numbers, img_path, caption))

    def on_send_pdf(self):
        numbers = self.get_valid_numbers(self.txt_phone_pdf)
        pdf_path = self.entry_pdf_path.get().strip()
        caption = self.txt_caption_pdf.get("1.0", tk.END).strip()

        if not numbers:
            messagebox.showerror("Error", "No valid phone numbers provided.")
            return
        if not pdf_path or not validate_file_path(pdf_path):
            messagebox.showerror("Error", "Invalid PDF path.")
            return

        self.run_in_thread(lambda: send_pdf(numbers, pdf_path, caption))

def run_gui():
    root = tk.Tk()
    app = WhatsAppSenderGUI(root) # assign it to prevent garbage collection
    root.mainloop()

if __name__ == "__main__":
    run_gui()
