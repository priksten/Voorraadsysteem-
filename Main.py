import tkinter as tk
from BarcodeScanner import BarcodeScanner
from BarcodeScanner_GUI import BarcodeScannerApp

def main():
    root = tk.Tk()
    scanner = BarcodeScanner()
    app = BarcodeScannerApp(root, scanner)
    root.mainloop()

if __name__ == "__main__":
    main()