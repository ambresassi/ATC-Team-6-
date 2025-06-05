import serial
import csv
import time

# Configuration
SERIAL_PORT = '/dev/tty.usbmodem68094401'  # Replace with your actual port
BAUD_RATE = 115200

# Open serial port
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

file_path = 'logs/talking_to_the_moon_Silicone.csv'

# Open CSV file for writing
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "peakToPeak"])  # Optional header

    print("Recording... Press Ctrl+C to stop.")
    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line.isdigit():  # Ensure the line is numeric (a valid peakToPeak value)
                timestamp = time.time()
                writer.writerow([timestamp, line])
                print(f"{timestamp}, {line}")
    except KeyboardInterrupt:
        print("Recording stopped.")
    finally:
        ser.close()