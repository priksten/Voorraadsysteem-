import tkinter as tk
from tkinter import messagebox, simpledialog
import threading

class BarcodeScannerApp:
    def __init__(self, root, scanner):
        self.root = root
        self.scanner = scanner
        self.scanner_thread = None
        self.text_window = None
        self.text_widget = None
        self.setup_gui()
        self.center_window(self.root, 200, 400)  # Initial window size: 400x300

    def setup_gui(self):
        self.root.title("Barcode Scanner")
        self.root.geometry("400x300")  # Set the initial size of the window (width x height)

        # Position the start/stop button
        self.start_stop_button = tk.Button(self.root, text="Start Scanner", command=self.toggle_scanner)
        self.start_stop_button.place(relx=0.1, rely=0.2, anchor=tk.W)

        # Position the quit button
        self.quit_button = tk.Button(self.root, text="Quit", command=self.on_closing)
        self.quit_button.place(relx=0.1, rely=0.8, anchor=tk.W)

        # Add a button to set the scan delay
        self.set_delay_button = tk.Button(self.root, text="Set Scan Delay", command=self.prompt_for_delay)
        self.set_delay_button.place(relx=0.1, rely=0.4, anchor=tk.W)

        # Add a label to display the current delay
        self.delay_label = tk.Label(self.root, text=f"Current Delay: {self.scanner.delay} seconds")
        self.delay_label.place(relx=0.1, rely=0.5, anchor=tk.W)

        # Add a button to open/close the text file viewer
        self.toggle_text_button = tk.Button(self.root, text="Toggle Scanner Log", command=self.toggle_text_window)
        self.toggle_text_button.place(relx=0.1, rely=0.6, anchor=tk.W)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def open_text_window(self):
        if self.text_window is None or not self.text_window.winfo_exists():
            # Create a new window
            self.text_window = tk.Toplevel(self.root)
            self.text_window.title("Scanner Logbook")
            self.text_window.protocol("WM_DELETE_WINDOW", self.close_text_window)

            # Align the text window with the left side of the main window
            main_window_x = self.root.winfo_x()
            main_window_y = self.root.winfo_y()
            self.text_window.geometry(f"300x400+{main_window_x - 300}+{main_window_y}")  # Adjust position

            # Create a text widget in the new window
            self.text_widget = tk.Text(self.text_window, wrap='word')
            self.text_widget.pack(expand=1, fill='both')

            # Load and display the content of barcode_text.txt
            self.update_text_widget()

            # Schedule periodic refresh every second
            self.schedule_text_widget_update()

    def update_text_widget(self):
        file_path = 'barcode_logbook.txt'
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                if self.text_widget is not None:
                    self.text_widget.delete(1.0, tk.END)
                    self.text_widget.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")

    def schedule_text_widget_update(self):
        if self.text_window and self.text_window.winfo_exists():
            self.update_text_widget()
            self.text_window.after(1000, self.schedule_text_widget_update)

    def prompt_for_delay(self):
        # Add option to change the time between scans
        delay = simpledialog.askinteger("Input", "Enter scan delay in seconds:", minvalue=1, maxvalue=60)
        if delay is not None:
            self.scanner.delay = delay
            self.delay_label.config(text=f"Current Delay: {self.scanner.delay} seconds")  # Update the delay label

    def center_window(self, window, width, height):
        # Places the menu window in the center of the screen
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def toggle_text_window(self):
        if self.text_window and self.text_window.winfo_exists():
            self.close_text_window()
        else:
            self.open_text_window()

    def close_text_window(self):
        if self.text_window and self.text_window.winfo_exists():
            self.text_window.destroy()
            self.text_window = None
            self.text_widget = None

    def toggle_scanner(self):
        if not self.scanner.running:
            self.start_scanner()
        else:
            self.stop_scanner()

    def start_scanner(self):
        if not self.scanner.running:
            self.scanner_thread = threading.Thread(target=self.scanner.run)
            self.scanner_thread.start()
            self.start_stop_button.config(text="Stop Scanner")

    def stop_scanner(self):
        if self.scanner.running:
            self.scanner.running = False
            self.scanner_thread.join()
            self.start_stop_button.config(text="Start Scanner")


    def on_text_window_close(self):
        self.text_window.destroy()
        self.text_window = None

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.stop_scanner()
            self.root.destroy()