import cv2
import time
import zxingcpp
import socket
import json
import os

class BarcodeScanner:
    def __init__(self, capture_device=0, delay=1):
        # The delay value specifies how long the camera waits between each scan
        self.capture_device = capture_device
        self.delay = delay  # Delay in seconds between scans
        self.cap = None
        self.last_scan_time = time.time()
        self.running = False
        self.latest_barcode_text = None

    def initialize_camera(self):
        # Accesses the camera.
        self.cap = cv2.VideoCapture(self.capture_device)
        if not self.cap.isOpened():
            raise Exception("Error: Could not open camera.")

    def process_barcodes_from_image(self, img):
        # Scans for barcodes. If found, prints the results in the python terminal.
        results = zxingcpp.read_barcodes(img)
        if results:
            for result in results:
                print(f'Found barcode:'
                      f'\n Text:    "{result.text}"'
                      f'\n Format:   {result.format}'
                      f'\n Content:  {result.content_type}'
                      f'\n Position: {result.position}')
                self.handle_barcode_info(result.text)
        else:
            print("Could not find any barcode.")

    def handle_barcode_info(self, result_text):
        self.latest_barcode_text = result_text
        barcode_info = [result_text, '+'] # Verander de '+' naar een '-' om producten te verwijderen ipv toe te voegen.
        self.send_barcode(barcode_info)
        self.write_barcode_text_to_file(result_text)
    def send_barcode(self, barcode):
        """Deze functie stuurt een barcode naar de database-server"""
        HOST = "10.0.1.159"
        PORT = 65432

        try:
            barcode_str = json.dumps(barcode)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                # Barcode via encode omzetten naar byte-format. Dit is nodig omdat je alleen bytes kunt versturen.
                s.sendall(barcode_str.encode('utf-8'))
                print("Barcode verstuurd!")
                data = s.recv(1024)
                print(data.decode())
                # print(f"Received data")
        except socket.error as e:
            print(f"Failed to send barcode. Error: {e}")

    def write_barcode_text_to_file(self, text, filename='barcode_logbook.txt'):
        try:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            new_line = f"{timestamp}: {text}\n"

            # Check if file exists to prevent FileNotFoundError in case file doesn't exist initially
            file_exists = os.path.exists(filename)

            with open(filename, 'r+') as file:
                if file_exists:
                    # Read the existing contents
                    content = file.read()
                    # Move the file pointer to the beginning
                    file.seek(0)
                else:
                    # If file doesn't exist, write directly
                    content = ''

                # Write new line at the beginning
                file.write(new_line + content)

        except IOError as e:
            print(f"Error writing to file: {e}")

    def scanner_delay(self):
        # Adds a delay to the scanner to prevent repeated scans of the same product.
        current_time = time.time()
        if current_time - self.last_scan_time >= self.delay:
            self.last_scan_time = current_time
            return True
        return False

    def run(self):
        # Main loop for capturing and processing frames
        self.running = True
        self.initialize_camera()
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break
            cv2.imshow('Barcode Scanner', frame)
            if self.scanner_delay():
                self.process_barcodes_from_image(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()